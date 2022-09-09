#!/usr/bin/env bash
# version 0.1
# author: jogerj


YELLOW='[33m'
RED='[31m'
GREEN='[32m'
CYAN='[36m'
ENDCOLOR='[0m'

tempdir="/tmp/paimonmoe";
mkdir -p $tempdir;

echo "Fetching adb... please wait";
if [[ $OSTYPE == 'darwin'* ]]; then
  curl -Lo "$tempdir/platform-tools.zip" "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip";
  unzip -o "$tempdir/platform-tools.zip" -d "$tempdir";
  adb="$tempdir/platform-tools/adb";
elif [[ $OSTYPE == 'linux-gnu'* ]]; then
  curl -Lo "$tempdir/platform-tools.zip" "https://dl.google.com/android/repository/platform-tools-latest-linux.zip";
  unzip -o "$tempdir/platform-tools.zip" -d "$tempdir";
  adb="$tempdir/platform-tools/adb";
elif [[ $OSTYPE == 'linux-android'* ]]; then
  if [[ ! $(adb version | grep "Android Debug Bridge") ]]; then
    echo -e "${RED}You must first install adb. In Termux run 'apt update' then 'apt install android-tools termux-api'";
    exit;
  else
    adb="adb";
  fi;
fi;

echo -e "${YELLOW}Please connect your phone via USB and turn on USB debugging on your phone
Go to Developer options -> Allow USB debugging
Guide:${ENDCOLOR}";
echo -e "${CYAN}https://developer.android.com/studio/debug/dev-options#enable${ENDCOLOR}";
read -p "Press enter to continue";

listDevices="$($adb devices)"
if [[ $(echo -e $listDevices | grep -E 'unauthorized$') ]]; then
  echo -e "${YELLOW}Please authorize USB debugging on your phone!
Make sure 'Always allow from this computer' is checked!${ENDCOLOR}";
  read -p "Press enter to continue";
  listDevices="$($adb devices)";
fi;

if [[ $(echo -e $listDevices | grep -E 'device$') ]]; then
  echo -e "${YELLOW}Please open Genshin Impact and open Wish History${ENDCOLOR}";
  url="$(grep -m 1 -oE "https.+/log" <( $adb logcat -m 1 -e "OnGetWebViewPageFinish" ) )";
  echo -e "${CYAN}$url${ENDCOLOR}";
  if [[ $OSTYPE == 'darwin'* ]]; then
    echo -e "$url" | pbcopy;
  elif [[ $OSTYPE == 'linux-gnu'* ]]; then
    echo -e "$url" | xclip -selection c;
  elif [[ $OSTYPE == 'linux-android'* ]]; then
    echo -e "$url" | termux-clipboard-set;
  fi;
  echo -e "${GREEN}Link copied to clipboard, paste it back to paimon.moe${ENDCOLOR}";
else
  echo -e "${RED}Could not connect to android device! Check your USB debugging settings again!${ENDCOLOR}"  
fi;

rm -rf $tempdir
