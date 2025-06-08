from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.chrome.options import Options


def Login(number,password,driver,wait,log_callback):
    try:
        Update("Opening Your Dashboard",log_callback)
        UserID = number 
        Password = password 
        driver.get("https://www.codingal.com/")
        time.sleep(1)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()
        time.sleep(0.5)
        phone_input = wait.until(EC.presence_of_element_located((By.NAME, "phone")))
        phone_input.send_keys(UserID)
        time.sleep(0.5)
        #Click "Login with Password" Button
        login_btn_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]")))
        login_btn_1.click()
        time.sleep(0.5)
        #Enter Password
        password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_input.send_keys(Password)
        time.sleep(0.5)
        login_btn_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with password')]")))
        login_btn_2.click()
        time.sleep(5)  #Time Required to fetch User Name and Image
        ProfilePic = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Profile Image']"))) 
        time.sleep(2)
        TeacherNameElement = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex-col')]/h2"))
)       
        TeacherName = TeacherNameElement.text
        time.sleep(2)
        ProfilePicSource = ProfilePic.get_attribute("src")
        time.sleep(2)
        StoreUserDetails(ProfilePicSource,TeacherName)
        time.sleep(1)
        Update(f"Login Succesfull! Hello {TeacherName}",log_callback)
    except Exception as e:
        print(f"Error During Login:{e}")
        Update(f"Error During Login:",log_callback)


def Pending_Project_Count(driver,wait,log_callback=None):
    # Step 5: Navigate to Dashboard Project
    driver.get("https://www.codingal.com/teacher/dashboard/projects/")
    try:
        time.sleep(0.5)
        project_number = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'font-600') and contains(@class, 'text-lg') and contains(@class, 'text-yellow-200')]")))
        # project_number = driver.find_element(By.XPATH, "//p[contains(@class, 'font-600') and contains(@class, 'text-lg') and contains(@class, 'text-yellow-200')]")
        Pending_project = int(project_number.text)
        return Pending_project
    except Exception as e:
        Update(f"Could not find project count, assuming 0",log_callback)
        return 0

def Generate_Review(name,lesson):
    try:
        openings = [
            f"Congratulations {name} on completing {lesson}!",
            f"Awesome job on finishing {lesson}, {name}!",
            f"Well done {name} for submitting your {lesson} project!",
            f" {name}, great effort on your {lesson} work!",
            f"You did it, {name}! {lesson} is complete!"
        ]

        compliments = [
            f"{name}, your creativity really shines through in the {lesson} project.",
            f"I can see the effort and thought you've put into {lesson}, {name}.",
            f" {name}, you're developing some solid skills through your work on {lesson}.",
            f"You're getting better with every project, and {lesson} is a great example of that, {name}.",
            f"Your {lesson} submission reflects clear understanding and imagination, {name}.",
            f" {name}, this {lesson} project shows great progress from your previous submissions.",
            f"Impressive attention to detail in your {lesson} project, {name}.",
            f" {name}, your approach to solving challenges in {lesson} is evolving beautifully."
        ]

        encouragements = [
            f"Keep up the amazing work! {name} ",
            f"You're on the right path {name} — stay consistent!",
            f"Proud of your progress {name} . Keep going!",
            "Excited to see what you'll do next!",
            f"Keep pushing your limits {name} — you're doing great!",
            "Keep challenging yourself — the sky's the limit!"
        ]

        review_text = (
            f"{random.choice(openings)} "
            f"{random.choice(compliments)} {random.choice(compliments)} "
            f"{random.choice(encouragements)} {random.choice(encouragements)} "
        )
        return review_text
    except Exception as e:
        Review_text = f"Congratulations {name} on completing {lesson} ! Your dedication and effort are commendable. Your work showcases creativity and skill. Keep up the excellent work! Your achievements demonstrate your potential and promise for future success. Well done {name}!"
        return Review_text


def Review_Project(driver,wait,log_callback=None):
    try:
        time.sleep(1)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Review now')])[1]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)  # Allow time for scrolling
        driver.execute_script("arguments[0].click();", element)
        #Project Page
        #Find Student Name
        Student_Name_element = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Submitted by')]/preceding-sibling::p")))
        Student_Name = Student_Name_element.text  # Output: Student Name
        #Find Lesson Name
        Lesson_Name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Lesson')]"))
        )
        Lesson_Name = Lesson_Name_element.text
        # Update(f"Reviewing project for {Student_Name} - {Lesson_Name}",log_callback)
        #Review Now Button
        review_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Review now')]")))
        review_btn.click()
        #Write Review
        textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        #Review Text
        Review = Generate_Review(Student_Name,Lesson_Name)
        # Type text into the textarea
        textarea.send_keys(Review)
        #Enhance With AI
        try:
            enhance_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[.//span[text()='Enhance with AI']]")))
            enhance_button.click()
            time.sleep(3)
        except Exception as e:
            pass
        #Give Star
        stars = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rating-star")))
        given_stars = random.choice([3,4])
        # Click the 5th star (index 4 in zero-based index)
        stars[given_stars].click()
        review_project = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit review')]")))
        #Submit Button Click
        review_project.click()  
        Update(f"Review completed successfully for {Student_Name}.",log_callback)
        time.sleep(1)
        back_to_Project = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(), 'Back to projects')])")))
        back_to_Project.click()
        time.sleep(1)
    except Exception as e:
        Update(f"Error during review",log_callback)
        print(f"Error during review {e}")


Review_Cancel = False
UserData ={}
Project_Count = None

def  Project_Count_Update():
    global Project_Count
    return Project_Count


def Update(message,log_callback=None):
    print(message)
    if log_callback:
        log_callback(message)

def Cancel():
    global Review_Cancel
    Review_Cancel = True

def StoreUserDetails(src,name):
    global UserData
    UserData["Name"] = name
    UserData["Picture"] = src

def GetUserDetails():
    return UserData


#Main Execution
def Start_Project_Review(number,password,log_callback = None):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    Login(number,password,driver,wait,log_callback)
    global Review_Cancel
    Review_Cancel = False 
    while True:
        Pending_projects = Pending_Project_Count(driver,wait,log_callback)
        global Project_Count
        Project_Count = Pending_projects
        if Pending_projects == 0:
            Update("All Projects review Completed.",log_callback)
            break
        if Review_Cancel :
            break
        try:
            Review_Project(driver,wait,log_callback)
            time.sleep(3)
        except Exception as e:
            Update(f"Error Inside Start_Review_Projct. Moving Forward !",log_callback)
            continue
    driver.quit()

