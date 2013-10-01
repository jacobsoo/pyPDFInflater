import zlib, sys, os, re

# Usage
def help_menu(cmd):
    print("Usage: ./%s <pdf_file.pdf>" % cmd)
    
# Main Program
def main(szFile):
    # Open the input file.
    hFile = open(szFile, "rb")
    contents = hFile.read()
    i = 1
    while True:
        compressed_contents = []
        pos = contents.find('FlateDecode')
        if pos == -1: pos = contents.find('/Fl') # Try to find its abbreviate
        if pos == -1: pos = contents.find('/#46#6c') # Try to find hexlified stream
        if pos == -1: pos = contents.find('/F#6c')
        if pos == -1: pos = contents.find('/#46l')
        if pos == -1: break                  # still not found, exit
        contents = contents[pos+4:]
        stream_found = contents.find('stream')
        compressed_contents = contents[stream_found+6:contents.find('endstream')]
        output_file = "decompressed_streams_" + str(i) + ".txt"
        
        bRes = True
        try:
            if compressed_contents[0] == ' ':
                compressed_contents = compressed_contents[1:]
            # Double check, it can be '\x0D\x0A' or '\x0D' or '\x0A' follow the 'stream'
            if compressed_contents[0] == '\r' or compressed_contents[0] == '\n':
                compressed_contents = compressed_contents[1:]
            if compressed_contents[0] == '\r' or compressed_contents[0] == '\n':
                compressed_contents = compressed_contents[1:]
            d = zlib.decompress(compressed_contents)
            i += 1
            hOut = open(output_file, "a+")
            hOut.write(d)
            hOut.close()
        except:
            bRes = False
    hFile.close()
    
if __name__ == '__main__':
    if len(sys.argv)<2:
        help_menu(sys.argv[0])
        sys.exit()
    main(sys.argv[1])