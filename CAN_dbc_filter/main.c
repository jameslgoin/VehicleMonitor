#include <stdio.h>
#include <stdlib.h>
#include "datenbasis.h"
#include "processFrame.h" 

// echo "(0.0) vcan0 001#8d00100100820100" | ./socketcanDecodeSignal ccl_test.dbc testFrame1
// echo "(0.1) vcan0 002#0C00057003CD1F83" | ./socketcanDecodeSignal ccl_test.dbc testFrame2
void printCallback(char *name, __u64 rawValue, double scaledValue,
		struct timeval tv, char *device)
{
	//printf("(%04ld.%06ld) %s %s: 0x%02llx %02.0f \n", tv.tv_sec, tv.tv_usec,
	//		device, name, rawValue, scaledValue);
	printf("%s:%02.0f\n", name, scaledValue);
	fflush(stdout);
}



int main(int argc, char **argv)
{
	char buf[100], device[100], ascframe[100];

	char *frameName, *signalName;
	struct can_frame cf;

	struct frame_struct *dataBase = NULL;
	struct signal_callback_list *callbackList = NULL;

	struct signal_struct *mySignal;
	struct frame_struct *myFrame;
	struct timeval tv;


	// Must include dbc file and file name with signals 
	if (argc < 1)
	{
		fprintf(stderr, "Usage:\n");
		fprintf(stderr,
				"%s Database Message1.Signal1 [Message2.Signal2 Message3.Signal3]\n",
				argv[0]);
		exit(1);
	}


	// read dbc
	if (readInDatabase(&dataBase, argv[1]))
	{
		fprintf(stderr, "Error opening Database %s\n", argv[1]);
		exit(1);
	}
	argc--;
	argv++;


	FILE * fp;
	char lineBuffer [500];

	fp = fopen(argv[1], "r");
	if(!fp)
	{
		fprintf(stderr, "Error opening file %s\n", argv[1]);
		exit(EXIT_FAILURE); 
	}

		
	// parse arguments (frames/signals which should be decoded)
	while((fgets(lineBuffer, 500, fp)) != NULL)
	{	

		char * frameName = lineBuffer;
		frameName[strcspn(frameName, "\r\n")] = 0;

		//frameName == line; //argv[2];
		signalName = strchr(frameName, '.');

		
		//printf("Trying to find: Frame: %s", frameName);
		if (signalName != NULL)
		{
			*signalName = 0;
			signalName++;
			//printf(", Signal: %s", signalName);
		}
		//printf("\n");
		myFrame = find_frame_by_name(dataBase, frameName);

		if (!myFrame)
		{
			fprintf(stderr, "Error finding Frame %s\n", frameName);
			exit(1);
		}

		if (NULL != signalName)
		{
			mySignal = find_signal_by_name(myFrame, signalName);
			if (!mySignal)
			{
				fprintf(stderr, "Error finding Signal %s\n", signalName);
				exit(1);
			}
		}
		else
		{
			mySignal = NULL;
		}
		add_callback(&callbackList, myFrame, mySignal, printCallback, 0);

		//printf("-- %s (0x%03x) ", myFrame->name, myFrame->canID);
		//if (signalName != NULL)
			//printf(" %s (%d [%d]) --", mySignal->name, mySignal->startBit,
			//		mySignal->signalLength);
		//printf("\n");	
	}

	fclose(fp);

	
	while (fgets(buf, 99, stdin))
	{

		if (sscanf(buf, "(%ld.%ld) %s %s", &tv.tv_sec, &tv.tv_usec, device,
				ascframe) != 4)
		{
			fprintf(stderr, "incorrect line format in logfile\n");
			return 1;
		}

		if (parse_canframe(ascframe, &cf))
		{
			return 1;
		}
		processFrame(callbackList, &cf, tv, device);
	}

	return 0;
}
