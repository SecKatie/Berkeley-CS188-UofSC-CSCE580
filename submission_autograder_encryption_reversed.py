#!/usr/local/bin/python3

import os
import sys
import re
import json
import base64
import math
import binascii
import primefac


def encrypt_message(msg, pubkey):
    log_of_pubkey = int(math.log(pubkey[1], 256))
    log_of_pubkey_plus_one = log_of_pubkey + 1
    format_string = '%%0%dx' % (log_of_pubkey_plus_one * 2)
    encoded_msg = msg.encode()
    list_of_blocks = []
    for i in range(0, len(encoded_msg), log_of_pubkey):
        block = encoded_msg[i:i + log_of_pubkey]
        block += b'\x00' * (log_of_pubkey - len(block))
        block_as_int = int(binascii.hexlify(block), 16)
        encrypted_num = pow(block_as_int, *pubkey)
        encoded_encrypted_num = binascii.unhexlify(
            (format_string % encrypted_num).encode())
        list_of_blocks.append(encoded_encrypted_num)
    return b''.join(list_of_blocks)


def decrypt_message(ciphertext, privkey):
    log_of_privkey = int(math.log(privkey[1], 256))
    log_of_privkey_plus_one = log_of_privkey + 1
    format_string = '%%0%dx' % (log_of_privkey_plus_one * 2)
    hexlifieded_msg = binascii.hexlify(ciphertext)
    decoded_message = hexlifieded_msg.decode()
    list_of_blocks = []
    for i in range(0, len(decoded_message), log_of_privkey_plus_one * 2):
        block = decoded_message[i:i + log_of_privkey_plus_one * 2]
        block_as_int = int(block, 16)
        decrypted_num = pow(block_as_int, *privkey)
        decoded_block = binascii.unhexlify(
            format_string % decrypted_num).decode().strip('\0')
        list_of_blocks.append(decoded_block)

    return "".join(list_of_blocks)


"""
submission_autograder.py: Local autograder client.
See README.md for a summary of how this program works.
Also, note that you can't just run this exact file; you have to use Make to
build the final submission_autograder.py file, then run that.
The build process (Makefile) #includes header.py and rsa.py here:
* header.py replaces the print statement with the Python 3 print() function.
* header.py replaces open with codecs.open; this must be done in header.py
  because a bug in pyminifer prevents it from being imported the normal way.
* rsa.py imports binascii and math.
* rsa.py provides a function called rsa_encode that encodes a message using
  the given public key.
"""

term_width = 79
project = 'reinforcement'
publickey = (33751518165820762234153612797743228623, 56285023496349038954935919614579038707)


def write_then_dots(i, width=term_width, indent=0, right_margin=5):
    print(' ' * indent + i + '.' * (width - len(i) - right_margin - indent), end='')
    sys.stdout.flush()


def write_with_indent(msg='DONE', indent=1):
    print(' ' * indent + msg)
    sys.stdout.flush()


def read_file(file_path, mode='r'):
    if not os.path.isfile(file_path):
        return '(not file)'
    with open(file_path, mode)as f:
        return f.read()


def print_entry():
    print('-' * term_width, end='\n\n')
    print('CS 188 Local Submission Autograder Tool')
    print('-' * term_width, end='\n\n')


""" Kept for informational purposes
def create_submission_token(extracted_files, raw_output, test_score):
    write_then_dots(
        'Generating submission token')
    dir_listing = os.listdir(
        extracted_files)
    work_dir_checksums = [calculate_checksum(os.path.join(
        extracted_files, i))for i in dir_listing]
    student_file_content = [read_file(os.path.join(
        extracted_files, i))for i in pAMwLbjTdBtxWXkHSnePGIDJRvmQVurCqNsKhyiFoOflYEcagz]
    final_output_message = {'project': project, 'local_time': time.strftime(time_format), 'gmt_time': time.strftime(time_format, time.gmtime()), 'duration_sec': time.time() - time.time(), 'score': test_score, 'raw_output': raw_output, 'self_contents': read_file(
        __file__), 'current_dir': os.getcwd(), 'current_dir_ls': os.listdir('.'), 'work_dir': extracted_files, 'work_dir_ls': dir_listing, 'work_dir_checksums': work_dir_checksums, 'work_dir_student_files': student_file_content, 'env': str(os.environ), 'os': platform.uname()}
    output_file_name = project + '.plaintext.token'
    with open(output_file_name, 'w') as f:
        f.write(json.dumps(final_output_message))
    encrypted_output_file_name = project + '.token'
    with open(encrypted_output_file_name, 'wb')as f:
        f.write(binascii.b2a_base64(encrypt_message(
            json.dumps(final_output_message), publickey)))
    write_with_indent()
    return encrypted_output_file_name
"""

def modify_element(data, element):
    if isinstance(data[element], list):
        editing = True
        while (editing):
            write_with_indent("Delete or add an element")
            for i in range(0, len(data[element])):
                write_with_indent(
                    str(i) + ": " + str(data[element][i]), indent=2)
            write_with_indent("ADD", indent=2)
            write_with_indent("DONE", indent=2)

            changewhat = input(":> ").replace('\n', ' ').replace('\r', '')

            if re.match("done", changewhat, re.IGNORECASE):
                editing = False
            elif re.match("add", changewhat, re.IGNORECASE):
                new_value = input("  Data: ").replace(
                    '\n', ' ').replace('\r', '')
                data[element].append(new_value)
            else:
                data[element].remove(data[element][int(changewhat)])
    else:
        if re.match("file", input("  Data from a [file] or [stdin]?: "), re.IGNORECASE):
            filename = input("  Filename: ").replace(
                '\n', ' ').replace('\r', '')
            data[element] = read_file(filename)
        else:
            newdata = input("  Data: ").replace('\n', ' ').replace('\r', '')
            data[element] = newdata

    return data


def modify_submission_token():
    write_then_dots("Opening plaintext token")
    input_file_name = project + '.plaintext.token'
    unencrypteddata = read_file(input_file_name)

    loadeddata = json.loads(unencrypteddata)
    write_with_indent()

    import re
    editing = True
    while (editing):
        write_with_indent("Which element do you want to change?")
        for i in loadeddata:
            write_with_indent(i + ": " + str(loadeddata[i])[:50].replace('\n', ' ').replace(
                '\r', '') + " : " + str(type(loadeddata[i])), indent=2)
        write_with_indent("DONE", indent=2)

        changewhat = input(":> ").replace('\n', ' ').replace('\r', '')

        if re.match("done", changewhat, re.IGNORECASE):
            editing = False
        else:
            loadeddata = modify_element(loadeddata, changewhat)

    write_then_dots("Saving data")
    with open(input_file_name, 'w') as f:
        f.write(json.dumps(loadeddata))
    write_with_indent()


def encrypt_submission_token(publickey):
    write_with_indent("Loaded key:", indent=0)
    print()

    write_with_indent('Public_Key: -e {} -n {}'.format(*publickey))
    print()

    write_then_dots('Encrypting submission token')

    input_file_name = project + '.plaintext.token'
    unencrypteddata = read_file(input_file_name)

    encrypted_output_file_name = project + '.token'
    with open(encrypted_output_file_name, 'wb') as f:
        f.write(binascii.b2a_base64(encrypt_message(unencrypteddata, publickey)))

    write_with_indent()


def decrypt_submission_token(privatekey):
    write_with_indent("Loaded keys:", indent=0)
    print()

    write_with_indent('Private_Key: -d {} -p {} -q {}'.format(*privatekey))
    print()

    write_then_dots('Loading encrypted token')
    input_file_name = project + '.token'
    with open(input_file_name, 'rb') as f:
        encrypteddata = f.read()
    write_with_indent()

    d = privatekey[0]
    n = privatekey[1] * privatekey[2]

    write_then_dots('Decrypting submission token')
    decrypted_output_file_name = project + '.plaintext.token'
    with open(decrypted_output_file_name, 'w') as f:
        f.write(decrypt_message(binascii.a2b_base64(encrypteddata), (d, n)))

    write_with_indent()


def generate_keys(size=2048):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import rsa

    if size < 512:
        write_with_indent('Size too small using default: 2048')
        size = 2048
    elif size % 512 != 0:
        write_with_indent('Size must be a multiple of 512 using default: 2048')
        size = 2048

    write_then_dots('Generating keys of size: {}'.format(size))

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    private_key_nums = private_key.private_numbers()
    public_key_nums = public_key.public_numbers()

    write_with_indent()
    print()

    write_with_indent('Generated Keys:')
    print()
    write_with_indent(
        'Private_Key: -d {} -p {} -q {}'.format(private_key_nums.d, private_key_nums.p, private_key_nums.q))
    write_with_indent(
        'Public_Key: -e {} -n {}'.format(public_key_nums.e, public_key_nums.n))


def crack_key(e, n):
    write_with_indent('Crack key: -e {} -n {}'.format(e, n))
    print()
    write_then_dots('Cracking Public_Key')
    factors_list = []
    for i in primefac.factorint(n):
        factors_list.append(i)

    p = 0
    q = 0

    if len(factors_list) == 2:
        p = factors_list[0]
        q = factors_list[1]

    n = p * q
    phi = (p - 1) * (q - 1)

    d = primefac._primefac.modinv(e, phi)

    privatekey = (d, p, q)
    write_with_indent()
    print()

    write_with_indent('Private Key found: -d {} -p {} -q {}'.format(*privatekey))


def write_final_output(test_score, output_file_name):
    print('\n' + '-' * term_width, end='\n\n')
    print('Final score: ' + test_score)
    print('Token file: ' + output_file_name, end='\n\n')
    print('Please make sure that this score matches the result produced by autograder.py.', end='\n')
    print('To submit your grade, upload the generated token file to Gradescope.', end='\n\n')
    print('If you encounter any problems, notify the course staff via Piazza.', end='\n\n')
    print('-' * term_width)


def run_submission_autograder():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--encrypt', action="store_const",
                        const=True, help='Encrypts a reinforcement.plaintext.token')
    parser.add_argument('--decrypt', action='store_const',
                        const=True, help='Decrypts a reinforcement.token')
    parser.add_argument('--modify', action="store_const", const=True,
                        help='Modifies a reinforcement.plaintext.token')
    parser.add_argument('--genkeys', action="store_const", const=True,
                        help='Generates private and public keys for encryption')
    parser.add_argument('--size', type=int,
                        help="The size of the keys to generate")
    parser.add_argument('--crackkey', action="store_const", const=True,
                        help='Attempts to factor and then recover a private key from a public key')
    parser.add_argument('--printcsce580key', action="store_const", const=True,
                        help='Prints the public key that was found in the csce580 reinforcement assignment')
    parser.add_argument(
        '-n', type=int, help='n component of public and private key')
    parser.add_argument('-p', type=int, help='p component of the private key')
    parser.add_argument('-q', type=int, help='q component of the private key')
    parser.add_argument('-e', type=int, help="e component of public key")
    parser.add_argument('-d', type=int, help='d component of private key')

    args = parser.parse_args()

    print_entry()

    if (args.modify is not None):
        modify_submission_token()
    elif (args.encrypt is not None):
        if (args.e is not None) & (args.n is not None):
            encrypt_submission_token(publickey=(args.e, args.n))
        else:
            write_with_indent("ERROR: You must provide a public key: -e xxx...xxx -n xxx...xxx are required")
    elif (args.decrypt is not None):
        if ((args.p is not None) & (args.q is not None) & (args.d is not None)):
            decrypt_submission_token(privatekey=(args.d, args.p, args.q))
        else:
            write_with_indent("ERROR: You must provide a private key: -d xxx...xxx -p xxx...xxx -q xxx...xxx are all required")
    elif (args.genkeys is not None):
        if (args.size is not None):
            generate_keys(args.size)
        else:
            generate_keys()
    elif (args.crackkey is not None):
        if (args.e is not None) & (args.n is not None):
            crack_key(args.e, args.n)
        else:
            write_with_indent("ERROR: You must provide a public key: -e xxx...xxx -n xxx...xxx are required")
    elif (args.printcsce580key is not None):
        publickey = (
            33751518165820762234153612797743228623, 56285023496349038954935919614579038707)
        write_with_indent('Key found in obfuscated file: -e {} -n {}'.format(*publickey), indent=0)
    else:
        parser.print_help()


if __name__ == '__main__':
    run_submission_autograder()
