#include <stdio.h>
#include <strings.h>

int main(void)
{
	char str[20];

	strcpy(str, "-889262067");
	int val = atoi(str);

	printf("%d", val);

	// We can always compare hex with integer (0x1234 == 1234)
	// And Hex with strings (0x1234 == abcd) (Just for the sake of example).
	// We don't need to convert hex to any form
	if (val == -0x35010ff3)
	{
		puts("\nDONE");
	}
}

