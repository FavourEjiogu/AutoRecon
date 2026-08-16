import ipaddress
import re

def is_valid_ipv4(target: str) -> bool:
    try:
        ip = ipaddress.IPv4Address(target)
        return True
    except ipaddress.AddressValueError:
        return False

def is_valid_ipv6(target: str) -> bool:
    try:
        ip = ipaddress.IPv6Address(target)
        return True
    except ipaddress.AddressValueError:
        return False

def is_valid_fqdn(target: str) -> bool:
    # A simple FQDN validator
    if not target or len(target) > 255:
        return False
    if target[-1] == ".":
        target = target[:-1]
    
    allowed = re.compile(r"^(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in target.split("."))

def is_private_ip(target: str) -> bool:
    try:
        ip = ipaddress.ip_address(target)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

def sanitize_target(target: str) -> str:
    """Strips whitespace and dangerous characters"""
    target = target.strip()
    # Strip basic shell metacharacters
    target = re.sub(r'[;&|`$<>\{\}\(\)\'"]', '', target)
    return target

def validate_target(target: str) -> dict:
    """Returns a dict with validation info: valid (bool), type (ip/domain), private (bool)"""
    target = sanitize_target(target)
    if not target:
        return {"valid": False, "error": "Target is empty"}
        
    if is_valid_ipv4(target) or is_valid_ipv6(target):
        is_private = is_private_ip(target)
        return {"valid": True, "type": "ip", "private": is_private, "target": target}
        
    if is_valid_fqdn(target):
        return {"valid": True, "type": "domain", "private": False, "target": target}
        
    return {"valid": False, "error": "Invalid format (not an IP or FQDN)"}
