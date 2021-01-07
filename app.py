import pickle
import streamlit as st

# loading the trained model
pickle_in = open('H1B_Model.pkl', 'rb')
classifier = pickle.load(pickle_in)


# defining the function which will make the prediction using the data which the user inputs
def prediction(job_title, soc_title, full_time_position,
               continued_employment, change_previous_employment,
               new_concurrent_employment, change_employer, amended_petition,
               employer_name, employer_city, employer_state, prevailing_wage,
               h1b_dependent, willful_violator, support_h1b):
    Y_N_dict = {'Y': 1, 'N': 0}

    emp_name_dict = {'TATA CONSULTANCY SERVICES LIMITED': 160,
                'DELOITTE CONSULTING LLP': 180,
                'INFOSYS LIMITED': 190,
                'ACCENTURE LLP': 150,
                'GOOGLE LLC': 200,
                'COGNIZANT TECHNOLOGY SOLUTIONS US CORP': 170,
                'CAPGEMINI AMERICA INC': 100,
                'ERNST & YOUNG U.S. LLP': 140,
                'AMAZON.COM SERVICES, INC.': 90,
                'MICROSOFT CORPORATION': 40}

    emp_state_dict = {'TX': 180,
                      'CA': 200,
                      'MA': 150,
                      'MD': 80,
                      'PA': 140,
                      'NJ': 190,
                      'NY': 170,
                      'WA': 100,
                      'MI': 130,
                      'IL': 160}

    emp_city_dict = {'ROCKVILLE': 30,
                     'PHILADELPHIA': 150,
                     'NEW YORK': 200,
                     'RICHARDSON': 90,
                     'SEATTLE': 110,
                     'CHICAGO': 190,
                     'MOUNTAIN VIEW': 180,
                     'EDISON': 160,
                     'SAN FRANCISCO': 170,
                     'COLLEGE STATION': 60}

    job_title_dict = {'SENIOR SOFTWARE ENGINEER': 'HIGH',
                      'JAVA DEVELOPER': 'HIGH',
                      'SOFTWARE DEVELOPER': 'MEDIUM',
                      'SOFTWARE ENGINEER': 'MEDIUM',
                      'PROGRAMMER ANALYST': 'MEDIUM',
                      'ASSISTANT PROFESSOR': 'MEDIUM',
                      'SENIOR SYSTEMS ANALYST JC60': 'MEDIUM',
                      'TECHNOLOGY LEAD - US - PRACTITIONER': 'VERY_HIGH',
                      'MANAGER JC50': 'MEDIUM',
                      'SENIOR SOFTWARE DEVELOPER': 'MEDIUM'}

    soc_title_dict = {'COMPUTER OCCUPATIONS, ALL OTHER': 'VERY_HIGH',
                      'SOFTWARE DEVELOPERS, APPLICATIONS': 'MEDIUM',
                      'COMPUTER SYSTEMS ANALYSTS': 'MEDIUM',
                      'MANAGEMENT ANALYSTS': 'HIGH',
                      'ACCOUNTANTS AND AUDITORS': 'HIGH',
                      'OPERATIONS RESEARCH ANALYSTS': 'HIGH',
                      'SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE': 'LOW',
                      'COMPUTER SYSTEMS ANALYST': 'MEDIUM',
                      'MECHANICAL ENGINEERS': 'MEDIUM',
                      'COMPUTER PROGRAMMERS': 'HIGH'}

    def wage_division(income):
        if income <= 50000:
            return "VERY_LOW"
        elif 50000 < income <= 70000:
            return "LOW"
        elif 70000 < income <= 90000:
            return "MEDIUM"
        elif 90000 < income <= 150000:
            return "HIGH"
        elif income >= 150000:
            return "VERY_HIGH"

    EMPLOYER_NAME = emp_name_dict.get(employer_name,0)
    EMPLOYER_CITY = emp_city_dict.get(employer_city,0)
    EMPLOYER_STATE = emp_state_dict.get(employer_state,0)

    # Pre-processing user input

    CONTINUED_EMPLOYMENT = int(continued_employment)
    CHANGE_PREVIOUS_EMPLOYMENT = int(change_previous_employment)
    NEW_CONCURRENT_EMPLOYMENT = int(new_concurrent_employment)
    CHANGE_EMPLOYER = int(change_employer)
    AMENDED_PETITION = int(amended_petition)

    H1B_DEPENDENT = Y_N_dict[h1b_dependent.strip().upper()]
    WILLFUL_VIOLATOR = Y_N_dict[willful_violator.strip().upper()]
    SUPPORT_H1B = Y_N_dict[support_h1b.strip().upper()]
    FULL_TIME_POSITION = Y_N_dict[full_time_position.strip().upper()]

    job_title = job_title_dict.get(job_title.strip(), 'NOT PRESENT')
    soc_title = soc_title_dict.get(soc_title.strip(), 'NOT PRESENT')

    if job_title == 'VERY_LOW':
        JOB_CLASS_LOW = 0
        JOB_CLASS_MEDIUM = 0
        JOB_CLASS_NOT_PRESENT = 0
        JOB_CLASS_VERY_HIGH = 0
        JOB_CLASS_VERY_LOW = 1
    elif job_title == 'LOW':
        JOB_CLASS_LOW = 1
        JOB_CLASS_MEDIUM = 0
        JOB_CLASS_NOT_PRESENT = 0
        JOB_CLASS_VERY_HIGH = 0
        JOB_CLASS_VERY_LOW = 0
    elif job_title == 'MEDIUM':
        JOB_CLASS_LOW = 0
        JOB_CLASS_MEDIUM = 1
        JOB_CLASS_NOT_PRESENT = 0
        JOB_CLASS_VERY_HIGH = 0
        JOB_CLASS_VERY_LOW = 0
    elif job_title == 'HIGH':
        JOB_CLASS_LOW = 0
        JOB_CLASS_MEDIUM = 0
        JOB_CLASS_NOT_PRESENT = 0
        JOB_CLASS_VERY_HIGH = 0
        JOB_CLASS_VERY_LOW = 0
    elif job_title == 'VER_HIGH':
        JOB_CLASS_LOW = 0
        JOB_CLASS_MEDIUM = 0
        JOB_CLASS_NOT_PRESENT = 0
        JOB_CLASS_VERY_HIGH = 0
        JOB_CLASS_VERY_LOW = 0
    else:
        JOB_CLASS_LOW = 0
        JOB_CLASS_MEDIUM = 0
        JOB_CLASS_NOT_PRESENT = 1
        JOB_CLASS_VERY_HIGH = 0
        JOB_CLASS_VERY_LOW = 0

    if soc_title == 'VERY_LOW':
        SOC_CLASS_LOW = 0
        SOC_CLASS_MEDIUM = 0
        SOC_CLASS_NOT_PRESENT = 0
        SOC_CLASS_VERY_HIGH = 0
        SOC_CLASS_VERY_LOW = 1
    elif soc_title == 'LOW':
        SOC_CLASS_LOW = 1
        SOC_CLASS_MEDIUM = 0
        SOC_CLASS_NOT_PRESENT = 0
        SOC_CLASS_VERY_HIGH = 0
        SOC_CLASS_VERY_LOW = 0
    elif soc_title == 'MEDIUM':
        SOC_CLASS_LOW = 0
        SOC_CLASS_MEDIUM = 1
        SOC_CLASS_NOT_PRESENT = 0
        SOC_CLASS_VERY_HIGH = 0
        SOC_CLASS_VERY_LOW = 0
    elif soc_title == 'HIGH':
        SOC_CLASS_LOW = 0
        SOC_CLASS_MEDIUM = 0
        SOC_CLASS_NOT_PRESENT = 0
        SOC_CLASS_VERY_HIGH = 0
        SOC_CLASS_VERY_LOW = 0
    elif soc_title == 'VER_HIGH':
        SOC_CLASS_LOW = 0
        SOC_CLASS_MEDIUM = 0
        SOC_CLASS_NOT_PRESENT = 0
        SOC_CLASS_VERY_HIGH = 0
        SOC_CLASS_VERY_LOW = 0
    else:
        SOC_CLASS_LOW = 0
        SOC_CLASS_MEDIUM = 0
        SOC_CLASS_NOT_PRESENT = 1
        SOC_CLASS_VERY_HIGH = 0
        SOC_CLASS_VERY_LOW = 0

    prevailing_status = wage_division(prevailing_wage)


    if prevailing_status == 'VERY_LOW':
        WAGE_CLASS_LOW = 0
        WAGE_CLASS_MEDIUM = 0
        WAGE_CLASS_NOT_PRESENT = 0
        WAGE_CLASS_VERY_HIGH = 0
        WAGE_CLASS_VERY_LOW = 1
    elif prevailing_status == 'LOW':
        WAGE_CLASS_LOW = 1
        WAGE_CLASS_MEDIUM = 0
        WAGE_CLASS_NOT_PRESENT = 0
        WAGE_CLASS_VERY_HIGH = 0
        WAGE_CLASS_VERY_LOW = 0
    elif prevailing_status == 'MEDIUM':
        WAGE_CLASS_LOW = 0
        WAGE_CLASS_MEDIUM = 1
        WAGE_CLASS_NOT_PRESENT = 0
        WAGE_CLASS_VERY_HIGH = 0
        WAGE_CLASS_VERY_LOW = 0
    elif prevailing_status == 'HIGH':
        WAGE_CLASS_LOW = 0
        WAGE_CLASS_MEDIUM = 0
        WAGE_CLASS_NOT_PRESENT = 0
        WAGE_CLASS_VERY_HIGH = 0
        WAGE_CLASS_VERY_LOW = 0
    elif prevailing_status == 'VER_HIGH':
        WAGE_CLASS_LOW = 0
        WAGE_CLASS_MEDIUM = 0
        WAGE_CLASS_NOT_PRESENT = 0
        WAGE_CLASS_VERY_HIGH = 0
        WAGE_CLASS_VERY_LOW = 0
    else:
        WAGE_CLASS_LOW = 0
        WAGE_CLASS_MEDIUM = 0
        WAGE_CLASS_NOT_PRESENT = 1
        WAGE_CLASS_VERY_HIGH = 0
        WAGE_CLASS_VERY_LOW = 0

    print([FULL_TIME_POSITION, CONTINUED_EMPLOYMENT, CHANGE_PREVIOUS_EMPLOYMENT, NEW_CONCURRENT_EMPLOYMENT,
           CHANGE_EMPLOYER, AMENDED_PETITION, EMPLOYER_NAME, EMPLOYER_CITY, EMPLOYER_STATE, H1B_DEPENDENT,
           WILLFUL_VIOLATOR, SUPPORT_H1B, WAGE_CLASS_LOW, WAGE_CLASS_MEDIUM, WAGE_CLASS_VERY_LOW, JOB_CLASS_LOW,
           JOB_CLASS_MEDIUM, JOB_CLASS_NOT_PRESENT, JOB_CLASS_VERY_HIGH, JOB_CLASS_VERY_LOW, SOC_CLASS_LOW,
           SOC_CLASS_MEDIUM, SOC_CLASS_NOT_PRESENT, SOC_CLASS_VERY_HIGH, SOC_CLASS_VERY_LOW])

    # Making predictions
    prediction_output = classifier.predict(
        [[FULL_TIME_POSITION, CONTINUED_EMPLOYMENT, CHANGE_PREVIOUS_EMPLOYMENT, NEW_CONCURRENT_EMPLOYMENT,
          CHANGE_EMPLOYER, AMENDED_PETITION, EMPLOYER_NAME, EMPLOYER_CITY, EMPLOYER_STATE, H1B_DEPENDENT,
          WILLFUL_VIOLATOR, SUPPORT_H1B, WAGE_CLASS_LOW, WAGE_CLASS_MEDIUM, WAGE_CLASS_VERY_LOW, JOB_CLASS_LOW,
          JOB_CLASS_MEDIUM, JOB_CLASS_NOT_PRESENT, JOB_CLASS_VERY_HIGH, JOB_CLASS_VERY_LOW, SOC_CLASS_LOW,
          SOC_CLASS_MEDIUM, SOC_CLASS_NOT_PRESENT, SOC_CLASS_VERY_HIGH, SOC_CLASS_VERY_LOW]])

    if float(prevailing_wage) <= 20000 or float(prevailing_wage) >= 1500000:
        prediction_output = 1

    if prediction_output == 0:
        predicted_output = 'Approved'
    else:
        predicted_output = 'Rejected'
    return predicted_output


# this is the main function in which we define our webpage
def main():
    # front end elements of the web page
    st.text('Author @sai Prashanth T S')
    st.text('saiprashanthts@gmail.com')
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit H1B Prediction ML App</h1> 
    </div> 
    """

    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html=True)

    # following lines create boxes in which user can enter data required to make prediction
    job_title = st.selectbox('JOB_TITLE', ('SOFTWARE ENGINEER', 'SOFTWARE DEVELOPER', 'SENIOR SYSTEMS ANALYST JC60',
                                           'SENIOR SOFTWARE ENGINEER', 'MANAGER JC50',
                                           'TECHNOLOGY LEAD - US - PRACTITIONER', 'ASSISTANT PROFESSOR',
                                           'PROGRAMMER ANALYST', 'JAVA DEVELOPER',
                                           'SENIOR SOFTWARE DEVELOPER', "Others"))
    soc_title = st.selectbox('SOC_TITLE', ('SOFTWARE DEVELOPERS, APPLICATIONS', 'COMPUTER OCCUPATIONS, ALL OTHER',
                                           'COMPUTER SYSTEMS ANALYST', 'COMPUTER SYSTEMS ANALYSTS',
                                           'SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE', 'COMPUTER PROGRAMMERS',
                                           'OPERATIONS RESEARCH ANALYSTS', 'MECHANICAL ENGINEERS',
                                           'ACCOUNTANTS AND AUDITORS', 'MANAGEMENT ANALYSTS',
                                           'Others'))
    full_time_position = st.selectbox('FULL_TIME_POSITION', ("Y", "N"))
    continued_employment = st.selectbox('CONTINUED_EMPLOYMENT', ("0", "1"))
    change_previous_employment = st.selectbox('CHANGE_PREVIOUS_EMPLOYMENT', ("0", "1"))
    new_concurrent_employment = st.selectbox('NEW_CONCURRENT_EMPLOYMENT', ("0", "1"))
    change_employer = st.selectbox('CHANGE_EMPLOYER', ("0", "1"))
    amended_petition = st.selectbox('AMENDED_PETITION', ("0", "1"))
    employer_name = st.selectbox('EMPLOYER_NAME', ('COGNIZANT TECHNOLOGY SOLUTIONS US CORP',
                                                   'INFOSYS LIMITED',
                                                   'TATA CONSULTANCY SERVICES LIMITED', 'GOOGLE LLC',
                                                   'ERNST & YOUNG U.S. LLP', 'CAPGEMINI AMERICA INC',
                                                   'DELOITTE CONSULTING LLP', 'AMAZON.COM SERVICES, INC.',
                                                   'MICROSOFT CORPORATION', 'ACCENTURE LLP', 'Others'))
    employer_city = st.selectbox('EMPLOYER_CITY', ('NEW YORK', 'COLLEGE STATION', 'CHICAGO', 'RICHARDSON',
                                                   'SAN FRANCISCO',
                                                   'MOUNTAIN VIEW', 'ROCKVILLE', 'EDISON', 'SEATTLE',
                                                   'PHILADELPHIA', 'Others'))
    employer_state = st.selectbox('EMPLOYER_STATE', ('CA', 'TX', 'NJ', 'NY', 'IL', 'MA', 'PA', 'MI', 'WA', 'MD',
                                                     'Others'))
    prevailing_wage = st.number_input("PREVAILING_WAGE")
    h1b_dependent = st.selectbox('H1B_DEPENDENT', ("Y", "N"))
    willful_violator = st.selectbox('WILLFUL_VIOLATOR', ("Y", "N"))
    support_h1b = st.selectbox('SUPPORT_H1B', ("Y", "N"))
    result = ""

    if st.button("Predict"):
        result = prediction(job_title, soc_title, full_time_position,
                            continued_employment, change_previous_employment,
                            new_concurrent_employment, change_employer, amended_petition,
                            employer_name, employer_city, employer_state, prevailing_wage,
                            h1b_dependent, willful_violator, support_h1b)
        st.success('Your H1B Prediction result is {}'.format(result))

    if st.button("About"):
        st.text('This is used to predict the H1B Prediction')


if __name__ == '__main__':
    main()

