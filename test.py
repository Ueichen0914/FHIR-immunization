import csv
import json
import requests
import datetime

headers = {'Content-Type': 'application/json'}
fhirbaseURL = "https://hapi.fhir.tw/fhir"

def patient(dic):
    with open(
            "JSON_template\Patient_template.json", "r", encoding="utf-8") as patient_json:
        patient = json.load(patient_json)
    for key, value in dic.items():
        if key == "LV_UUID":
            # 加入id
            patient["id"] = str(value)
        elif key == "SEX":
            # 判斷性別
            if value == "1":
                info = "male"
            elif value == "2":
                info = "female"
            elif value == "3" | "4":
                info = "other"
            elif value == "9":
                info = "unknown"
            patient["gender"] = info
        elif key == "BIRTH_Y":
            # 判斷生日(民國)，放入svalue
            ivalue = int(value)
            if ivalue < 2000000:
                ivalue += 19110000
            svalue = str(ivalue)
            # 西元加入"-"放入ssvalue
            ssvalue = svalue[:4] + "-" + svalue[4:6] + "-" + svalue[6:8]
            patient["birthDate"] = ssvalue
        elif key == "RESID":
            # 加入地址
            patient["address"][0]["postalCode"] = str(value)
        elif key == "FU_DT":
            # 判斷生日(民國)，放入svalue
            ivalue = int(value)
            if ivalue < 2000000:
                ivalue += 19110000
            svalue = str(ivalue)
            # 西元加入"-"放入ssvalue
            ssvalue = svalue[:4] + "-" + svalue[4:6] + "-" + svalue[6:8]
            patient["deceasedDateTime"] = ssvalue
        # deceased boolean 和 datetime擇一
        # elif key == "VSTATUS":
        #     if value == "1":
        #         info = False
        #     else:
        #         info = True
        #     patient["deceasedBoolean"] = info
        else:
            pass
    return patient



def observation_height(dic):
    with open(
            "JSON_template\Observation_Body_height.json", "r", encoding="utf-8") as height_json:
        height = json.load(height_json)
    for key, value in dic.items():
        if key == "HEIGHT":
            height["valueQuantity"]["value"] = float(value)
        elif key == "LV_UUID":
            height["subject"]["reference"] = "Patient/" + str(value)
        else:
            pass
    height["effectiveDateTime"] = str(datetime.date.today())
    return height

    def observation_SSF(dic, num):
        with open(
            "JSON_template\SSF_template.json", "r", encoding="utf-8") as SSF_json:
            SSF = json.load(SSF_json)
        SSFNUM = "SSF" + num
        SSF["code"]["coding"]["code"] = SSFNUM
        for key, value in dic.items():
            if key == SSFNUM:
                SSF["code"]["coding"][0]["display"] = str(value)
            elif key == "LV_UUID":
                SSF["subject"]["reference"] = "Patient/" + str(value)
            else:
                pass
        SSF["effectiveDateTime"] = str(datetime.date.today())
        return SSF

file = "csv_example\FHIR_test.csv"
with open(file) as f:
    text = csv.DictReader(f)
    # Put Patient
    for line in text:
        json_patient = json.dumps(patient(line))
        for key, value in line.items():
            if key == "LV_UUID":
                fhirresourceURL = fhirbaseURL + "/Patient/" + str(value)
        r_patient = requests.put(
            fhirresourceURL, headers=headers, data=json_patient)
        print(r_patient.text)
        # Post Height
        json_ob = json.dumps(observation_height(line))
        fhirresourceURL = fhirbaseURL + "/Observation"
        r_ob = requests.post(
            fhirresourceURL, headers=headers, data=json_ob)
        print(r_ob.text)
        # Post SSF
        for i in range(10):
            json_ob = json.dumps(observation_SSF(line, str(i+1)))
            fhirresourceURL = fhirbaseURL + "/Observation"
            r_ob = requests.post(
                fhirresourceURL, headers=headers, data=json_ob)
            print(r_ob.text)