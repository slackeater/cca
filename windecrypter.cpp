#include "stdafx.h"
#include <Windows.h>
#include <dpapi.h>
#include <string>
#include <Wincrypt.h>
#include <ShlObj.h>
#include <algorithm>
#include <stdexcept>

std::string hex_to_string(const std::string& input)
{
    static const char* const lut = "0123456789ABCDEF";
    size_t len = input.length();
    if (len & 1) throw std::invalid_argument("odd length");

    std::string output;
    output.reserve(len / 2);
    for (size_t i = 0; i < len; i += 2)
    {
        char a = input[i];
        const char* p = std::lower_bound(lut, lut + 16, a);
        if (*p != a) throw std::invalid_argument("not a hex digit");

        char b = input[i + 1];
        const char* q = std::lower_bound(lut, lut + 16, b);
        if (*q != b) throw std::invalid_argument("not a hex digit");

        output.push_back(((p - lut) << 4) | (q - lut));
    }
    return output;
}

int _tmain(int argc, _TCHAR* argv[])
{
	DATA_BLOB in, out;
	std::string pwd = argv[1], password;
	std::string decString = hex_to_string(pwd);

	in.pbData = (BYTE *) decString.data(); 
	in.cbData = decString.length();

	//// decrypt using DPAPI
	if (CryptUnprotectData(&in, NULL, NULL, NULL, NULL, 1, &out)) {
		password = (char*)out.pbData;
		password[out.cbData] = 0;
		LocalFree(out.pbData);
	} else {
		password = "<decryption failed>";
	}

	printf("%s", password.c_str());
}
