#!/bin/bash

rm output.wav
# Check if argument is provided
if [ -z "$1" ]
then
    echo "No language supplied"
    exit 1
fi

# Assign the argument to a variable based on your specifications
echo "LANGUAGE $1"
case $1 in
    'de')
        LANGUAGE='de-DE'
        ;;
    'en')
        LANGUAGE='en-US'
        ;;
    'it')
        LANGUAGE='it-IT'
        ;;
    *)
        echo "Invalid language"
        LANGUAGE='en-US'
	#exit;
        ;;
esac

# Check if file exists
if [ ! -f "textfile.txt" ]; then
    echo "File textfile.txt does not exist."
    exit 1
fi

# Read the contents of the file into a variable
CONTENTS_OF_TEXTFILE=$(cat textfile.txt)

echo $CONTENTS_OF_TEXTFILE

# Call pico2wave with the appropriate arguments
pico2wave -l $LANGUAGE -w output_slow.wav "${CONTENTS_OF_TEXTFILE}"
# Speed up things
sox output_slow.wav output.wav tempo 1.2
rm output_slow.wav
rm textfile.txt
