import smtplib
from email.mime.text import MIMEText

from config import cfg
from env_var import read_env_var

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("./templates"), autoescape=select_autoescape()
)


class SmtpClient:
    __server = None

    def __init__(self):
        self.__server = smtplib.SMTP_SSL(cfg["smtp"]["Host"], cfg["smtp"]["Port"])

        resolvedUsername = read_env_var(cfg["smtp"]["User"])
        resolvedPassword = read_env_var(cfg["smtp"]["Password"])

        self.__server.login(resolvedUsername, resolvedPassword)
        debugLevel = cfg["smtp"]["DebugLevel"]
        self.__server.set_debuglevel(int(debugLevel))

    def send_email_on_unauthorized(
        self, rfidValue: str, userId: str, entryTimes: list[str]
    ):
        fromAddr = read_env_var(cfg["smtp"]["FromAddress"])
        toAddr = read_env_var(cfg["smtp"]["ToAddress"])

        template = env.get_template("unauthorized.html")

        renderedTemplate = template.render(
            rfidValue=rfidValue, userId=userId, entryTimes=entryTimes
        )

        msg = MIMEText(renderedTemplate)
        msg.set_type("text/html")
        msg["Subject"] = "Többszörös tiltott belépési kísérlet"
        msg["From"] = fromAddr
        msg["To"] = toAddr

        self.__server.sendmail(fromAddr, toAddr, msg.as_string())

    def send_mail_on_critical_temperature(
        self,
        max_temp: float,
        timestamp: str,
        userId: str,
        rfidValue: str,
        imageData: str,
    ):
        fromAddr = read_env_var(cfg["smtp"]["FromAddress"])
        toAddr = read_env_var(cfg["smtp"]["ToAddress"])

        template = env.get_template("critical_temp.html")

        renderedTemplate = template.render(
            max_temp=max_temp,
            timestamp=timestamp,
            userId=userId,
            rfidValue=rfidValue,
            image_data=imageData,
        )

        msg = MIMEText(renderedTemplate)
        msg.set_type("text/html")
        msg["Subject"] = "Kritikus hőmérséklet elérve!"
        msg["From"] = fromAddr
        msg["To"] = toAddr

        attachment = MIMEText(imageData, "base64", "utf-8")
        attachment.add_header(
            "Content-Disposition", "attachment", filename="temperature_graph.png"
        )
        attachment.add_header("Content-ID", "<temperature_graph>")
        msg.attach(attachment)
        msg["Content-Type"] = 'multipart/mixed; boundary="boundary"'

        self.__server.sendmail(fromAddr, toAddr, msg.as_string())


smtp = SmtpClient()
