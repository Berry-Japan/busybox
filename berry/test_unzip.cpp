#include <iostream>
#include <string>
//#include <cctype>
#include <stdio.h>

using namespace std;

int main()
{
	string lCommand = "unzip -l -qq \"" /*+ aFileName*/"/root/soft/skins/akari.zip" /*+*/ "\"";   //get info
	FILE *f = popen(lCommand.c_str(), "r");

	bool eof = false;
	while(!eof)
	{
		char line[301];
		char lUncompName[300];
		if (fgets(line, 300, f) <= 0)
		{
			eof = true;
			break;
		}

		/*if (processLine(line, &mSize, lUncompName))
		{
			lGoodName = lUncompName;
			bFound = true;
			break;
		}*/
		printf("%s", line);
	}

	pclose(f);
}
