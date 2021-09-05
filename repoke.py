from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import click
import logging


@click.command("repoke")
@click.argument("login")
@click.argument("password")
@click.option('-r', '--refresh-delay', default=7)
@click.option('-p', '--poke-delay', default=2)
def repoke(login, password, refresh_delay, poke_delay):

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path="geckodriver", options=options)
    driver.get("http://facebook.com/pokes")

    logging.info("Logging started")

    driver.find_element_by_xpath('//button[@title="Akceptuj wszystkie"]').click()
    driver.find_element_by_name("email").send_keys(login)
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_name("login").click()

    logging.info("Logged")

    while True:
        time.sleep(refresh_delay)

        pokes = driver.find_elements_by_xpath("//span[text()='Odpowiedz na zaczepkę']")

        if pokes:
            logging.info(f"{len(pokes)} pokes detected")

        for poke in pokes:
            poke.click()
            time.sleep(poke_delay)

        driver.refresh()


if __name__ == "__main__":
    logging.basicConfig(format='Date-Time : %(asctime)s: - %(message)s', level=logging.INFO)
    repoke()
