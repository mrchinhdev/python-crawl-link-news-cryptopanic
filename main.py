from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

### scoll mouse 
def wheel_element(element, deltaY = 120, offsetX = 0, offsetY = 0):
  error = element._parent.execute_script("""
    var element = arguments[0];
    var deltaY = arguments[1];
    var box = element.getBoundingClientRect();
    var clientX = box.left + (arguments[2] || box.width / 2);
    var clientY = box.top + (arguments[3] || box.height / 2);
    var target = element.ownerDocument.elementFromPoint(clientX, clientY);

    for (var e = target; e; e = e.parentElement) {
      if (e === element) {
        target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
        target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
        return;
      }
    }    
    return "Element is not interactable";
    """, element, deltaY, offsetX, offsetY)
  if error:
    raise WebDriverException(error)



options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get('https://cryptopanic.com/')
driver.maximize_window()
time.sleep(2)

# scroll mouse
for i in range(1,10):
    for i in range (1,100):
        html = driver.find_element(By.TAG_NAME,'html')
        html.send_keys(Keys.ARROW_DOWN)
    elm = driver.find_element(By.TAG_NAME,"html")
    wheel_element(elm, 120)
    time.sleep(1)

elems = driver.find_elements(By.XPATH, "//a[@href]")
for elem in elems:
    link = elem.get_attribute("href")
    if 'news' in str(link):
        print(link)
        if len(link)>50:
            with open("link.txt",'a',encoding = 'utf-8') as f:
                        f.write(link+ '\n')
                        
# Filter duplicate links (lọc liên kết trùng lặp)
listlink = open('link.txt','r',encoding='utf-8').read().splitlines()
listlink = list(set(listlink))
update = '\n'.join(listlink)
z = open('link.txt','w',encoding='utf-8')
z.write(update)
z.close()
driver.close()

