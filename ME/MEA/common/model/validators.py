import socket

def is_valid_ip(ip_addr):
    """Validates if the specified ip_addr is a legal IP address.
    """
    try:
        socket.inet_aton(str(ip_addr))
    except socket.error:
        return False

    return True