import random
import string


def generate_random_string(n=8):
    """Generate random string could be used for IDs, etc"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

print generate_random_string(n=20)