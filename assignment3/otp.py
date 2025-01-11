import pyotp
import qrcode
import sys
import time
import signal
from datetime import datetime

#signal handler to exit the program
def interrupt_exit(sig, frame):
    print("\nOTP generation stopped.")
    sys.exit(0)

#set up signal handler for Ctrl+C (SIGINT)
signal.signal(signal.SIGINT, interrupt_exit)

#secret is the key
def generate_qr(secret, label, issuer):
    uri = f"otpauth://totp/{issuer}:{label}?secret={secret}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
    print(f"URI for QR code: {uri}")
    
    #generate QR code
    qr = qrcode.make(uri)
    qr.save("otp_qr.png")
    print("QR code saved as 'otp_qr.png'. Scan it with Google Authenticator.")

def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    return otp

def main():
    if len(sys.argv) < 2:
        print("Usage: ./submission --generate-qr or --get-otp")
        sys.exit(1)
    
    if sys.argv[1] == "--generate-qr":
        #Example usage: ./submission --generate-qr
        secret = pyotp.random_base32()
        label = "bakerset@oregonstate.edu" #change if you want to use the OTP for yourself
        issuer = "Google"
        generate_qr(secret, label, issuer)

    elif sys.argv[1] == "--get-otp":
        #Example usage: ./submission --get-otp <secret>
        if len(sys.argv) < 3:
            print("Usage: ./submission --get-otp <secret>")
            sys.exit(1)
        secret = sys.argv[2]
        try:
            while True:
                otp = generate_otp(secret)
                print(f"Current OTP: {otp}")
                time.sleep(30)  #wait for the next 30-second period to generate the next OTP
        except KeyboardInterrupt:
            #exit if interrupted
            interrupt_exit(None, None)

    else:
        print("Invalid argument. Use --generate-qr or --get-otp.")
        sys.exit(1)

if __name__ == "__main__":
    main()
