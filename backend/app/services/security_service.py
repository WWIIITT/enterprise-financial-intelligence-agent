from __future__ import annotations

import hashlib
import re

from app.api.schemas import SecurityCheckRequest, SecurityCheckResponse, SecurityFinding, TraceStep
from app.services.metadata_service import record_security_audit


EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}(?!\d)")
SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
SECRET_PATTERN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{16,}|api[_-]?key[=:][A-Za-z0-9_.-]{12,}|token[=:][A-Za-z0-9_.-]{12,})\b",
    re.IGNORECASE,
)

PROMPT_INJECTION_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"ignore (?:all )?(?:previous|prior) instructions", re.IGNORECASE), "ignore_previous_instructions"),
    (re.compile(r"reveal (?:the )?(?:system prompt|developer message|hidden instructions)", re.IGNORECASE), "reveal_system_prompt"),
    (re.compile(r"(?:disable|bypass|override) (?:the )?(?:policy|guardrail|compliance|security)", re.IGNORECASE), "bypass_policy"),
    (re.compile(r"exfiltrate|extract secrets|steal credentials", re.IGNORECASE), "secret_exfiltration"),
    (re.compile(r"act as (?:dan|jailbreak|unfiltered)", re.IGNORECASE), "jailbreak_roleplay"),
)


def run_security_check(request: SecurityCheckRequest, persist: bool = True) -> SecurityCheckResponse:
    masked_message = request.message
    findings: list[SecurityFinding] = []
    policy_tags: set[str] = set()

    masked_message, pii_findings = _mask_pii(masked_message)
    findings.extend(pii_findings)
    if pii_findings:
        policy_tags.add("data-privacy")
        policy_tags.add("pii-handling")

    injection_findings = _detect_prompt_injection(request.message)
    findings.extend(injection_findings)
    if injection_findings:
        policy_tags.add("prompt-injection")
        policy_tags.add("ai-usage-policy")

    action = _decide_action(findings)
    risk_level = _risk_level(findings, action)
    response = SecurityCheckResponse(
        status="completed",
        risk_level=risk_level,
        action=action,
        masked_message=masked_message,
        findings=findings,
        policy_tags=sorted(policy_tags),
        recommended_handling=_recommended_handling(action),
        trace=[
            TraceStep(step="security_preflight", detail=f"Security action {action} with {len(findings)} finding(s)."),
        ],
    )

    if persist:
        record_security_audit(
            message_hash=hash_message(request.message),
            role=request.role,
            risk_level=response.risk_level,
            action=response.action,
            finding_count=len(response.findings),
        )

    return response


def build_security_block_answer(result: SecurityCheckResponse) -> str:
    return (
        "## Summary\n"
        "This request was blocked by the governance preflight because it appears to ask for unsafe model behavior.\n\n"
        "## Governance Findings\n"
        + "\n".join(f"- {finding.description}" for finding in result.findings)
        + "\n\n## Required Handling\n"
        "- Rephrase the request without asking the system to bypass policies, reveal hidden instructions, or expose secrets."
    )


def hash_message(message: str) -> str:
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def _mask_pii(message: str) -> tuple[str, list[SecurityFinding]]:
    findings: list[SecurityFinding] = []
    masked = message
    replacements = (
        (EMAIL_PATTERN, "[EMAIL]", "email", "Email address was masked."),
        (PHONE_PATTERN, "[PHONE]", "phone", "Phone number was masked."),
        (SSN_PATTERN, "[SSN]", "ssn", "US SSN-like identifier was masked."),
        (CREDIT_CARD_PATTERN, "[PAYMENT_CARD]", "payment_card", "Payment card-like number was masked."),
        (SECRET_PATTERN, "[SECRET]", "secret", "API key or token-like secret was masked."),
    )
    for pattern, replacement, finding_type, description in replacements:
        if pattern.search(masked):
            masked = pattern.sub(replacement, masked)
            severity = "high" if finding_type in {"ssn", "payment_card", "secret"} else "medium"
            findings.append(
                SecurityFinding(
                    category="pii",
                    finding_type=finding_type,
                    severity=severity,
                    description=description,
                    replacement=replacement,
                )
            )
    return masked, findings


def _detect_prompt_injection(message: str) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for pattern, finding_type in PROMPT_INJECTION_PATTERNS:
        if pattern.search(message):
            findings.append(
                SecurityFinding(
                    category="prompt_injection",
                    finding_type=finding_type,
                    severity="high",
                    description=f"Prompt injection pattern detected: {finding_type}.",
                )
            )
    return findings


def _decide_action(findings: list[SecurityFinding]) -> str:
    if any(finding.category == "prompt_injection" for finding in findings):
        return "block"
    if findings:
        return "mask"
    return "allow"


def _risk_level(findings: list[SecurityFinding], action: str) -> str:
    if action == "block" or any(finding.severity == "high" for finding in findings):
        return "high"
    if findings:
        return "medium"
    return "low"


def _recommended_handling(action: str) -> str:
    if action == "block":
        return "Block the request and ask the user to remove policy-bypass or secret-exfiltration instructions."
    if action == "mask":
        return "Continue with the masked message and avoid storing raw sensitive text."
    return "Continue normal agent routing."
