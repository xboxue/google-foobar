import base64

MESSAGE = "A0UcDRYGHREcX1VfWEUIChAEDEVDWFIGFw4DHRQCDQdIWE9FXwccDBAAFQcLX1lFXwcJHhoXDBFI WE9FXwsBGwcAHAsNFBBCVEJIGRYNEQcZHRgAFhZIWE9FXxcBFBoGEwcLX1lFXxAOGhcMDBFIWE9F XxEOHhBCVEJIHhoKX0JVWFISEQxOXwg="

KEY = "xboxue"

result = []
for i, c in enumerate(base64.b64decode(MESSAGE)):
    result.append(chr(ord(c) ^ ord(KEY[i % len(KEY)])))

print("".join(result))
