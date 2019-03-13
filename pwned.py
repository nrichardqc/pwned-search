import hashlib
import requests
import sys


def lookup_pwned_api(pwd):
    """Returns hash and number of times password was seen in pwned database.

    Args:
        pwd: password to check

    Returns:
        A (sha1, count) tuple where sha1 is SHA1 hash of pwd and count is number
        of times the password was seen in the pwned database.  count equal zero
        indicates that password has not been found.

    Raises:
        RuntimeError: if there was an error trying to fetch data from pwned
            database.
    """
    sha1pwd = hashlib.sha1(pwd.encode('ascii')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return sha1pwd, count


def main():
    while True:
        pwd = input('Enter your clear password (empty to exit) : ')
        if (not pwd):
            break
        sha1pwd, count = lookup_pwned_api(pwd)
        if count:
            print(pwd, "was found")
            print("Hash {0}, {1} occurrences".format(sha1pwd, count))
        else:
            print(pwd, "was not found")
    return 0

if __name__ == '__main__':
    sys.exit(main())
