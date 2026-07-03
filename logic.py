dts = "0123456789ABCDEF"

def validate_symbols(value: str, base: int) -> bool:
    if not value:
        return False
    value = value.upper().strip()
    allowed = dts[:base]
    for ch in value:
        if ch not in allowed:
            return False
    return True

def to_decimal(value: str, base_from: int) -> int:
    value = value.upper().strip()
    if not value:
        raise ValueError("Пустая строка")
    if not validate_symbols(value, base_from):
        raise ValueError(f"Недопустимые символы для системы {base_from}")
    
    if base_from == 10:
        return int(value)
    return int(value, base_from)

def from_decimal(number: int, base_to: int) -> str:
    if number == 0:
        return "0"
    digits = dts[:base_to]
    result = ""
    n = number
    while n > 0:
        result = digits[n % base_to] + result
        n //= base_to
    return result

def convert(value: str, base_from: int, base_to: int) -> str:
    if base_from == base_to:
        return value.strip().upper()
    decimal = to_decimal(value, base_from)
    return from_decimal(decimal, base_to)
