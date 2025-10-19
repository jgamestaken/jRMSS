
# jRMSS

![badge](https://img.shields.io/badge/This%20project%20runs-Python-green)

jgamestaken **R**eady-to-use **M**ail **S**ending **S**ervice is a program targeted at sending automated emails(e.g. for a company's no-reply). This software is free-to-use, you can copy and adapt it in any way you want, however, you may not sell this software.

jRMSS is supposed to provide others of ease when installing their own mail service- instead of also having to code this!
# Deployment

To run this Python project, it's recommended to create a **virtual environment**. You can set it up as follows (assuming you have Python & git installed already). This example works on Linux & Windows, although some commands are different. Please check before executing!

### Step 1
**Clone the repository with git**

```bash
  git clone https://github.com/jgamestaken/jRMSS && cd jRMSS
```

This will create a directory within your current working directory called "jRMSS".

### Step 2
**Create your virtual environment**

```bash
  python -m venv env
```

This will create a new Python virtual environment called "env".

### Step 3
**Enter your virtual environment**

⚠️ This command is OS-specific

*LINUX*
```bash
  source env/bin/activate
```

*WINDOWS*
```bash
  .\env\Scripts\activate
```

These commands enable your **virtual environment**, if this worked, you'll now see *(env)* in your terminal.

### Step 4
**Install requirements**

```bash
  pip install -r requirements.txt
```

This will install all the necessary requirements directly into your virtual environment.

### Step 5
**Run the app**

```bash
  python app.py
```

This will run the app in that terminal. To run the app again later, you will need to enter your virtual environment again.

### Final advice

If you're planning on using this in production, use a systemd service and the `scripts/run.sh` or `scripts/run.bat` scripts to run this via a systemd service (on Linux) or a startup service (on Windows).

A custom service file is also already provided in `scripts/jRMSS.service`.
# Documentation

Reminder, always check your port before sending files, the default isn't 80, it's **7979**.

## Send an email

```http
  POST /
```

### Expects

This function expects a JSON-like input.

| JSON Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `to` | `string` | **Required** - The recipient email address |
| `subject` | `string` | **Required** - The email subject |
| `content` | `array` | **Required** - **See format below** |

### Returns

This function returns a JSON-like output.

| Return parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `sent` | `boolean` | Whether the email was sent |
| `message` | `string` | Any notes to how the email was sent |

### Content format

Sending content always starts with an array, within that array, you can put an infinite amount of dictionaries(see below).

| JSON Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `data` | `string` | **Required** - The data to be sent |
| `type` | `string` | **Required** - The data type - **text** OR **html** |

### Example JSON submission

The JSON below shows a basic input to this function.

```json
{
    "to": "your@email_address.com",
    "subject": "Your subject",
    "content": [
        {
            "data": "Your email data",
            "type": "text"
        },

        {
            "data": "<html></html>",
            "type": "html"
        }
    ]
}
```

The JSON below shows a basic return from this function.

```json
{
    "sent": true,
    "message": "Mail sent"
}
```

## Customizing your .env

The .env file provides you with handy comments you can use to set it up for your own!


