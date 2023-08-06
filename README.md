# 3DPrint-Notifier
This is a simple yet effective Python script that monitors your 3D printer(s) for completion of print jobs. As soon as a print job completes it sends you an email similar as the one in the screenshot below.

<img src="/Screenshots/ScreenShot.png" style="width:405px;" alt="Screenshot of notification">

## Installation
* Modify the files ```3dprintnotifier.py``` and ```sendmail2.php``` by entering your details like IP addresses of your printer(s) and your email address.
* Place the files under PHP on your hosted webserver.
* Place the file ```3dprintnotifier.py``` somewhere on a PC that is running all the time.
* Make it executable by using ```chmod +x 3dprintnotifier.py```

## Running in the background
Set it in your crontab using ```crontab -e``` and adding the line
```
@reboot /home/user/somewhere/3dprintnotifier.py
```
As long as the script runs it monitors your 3D printer(s).****
