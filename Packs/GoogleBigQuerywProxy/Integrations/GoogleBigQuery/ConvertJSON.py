cred = {
  "type": "service_account",
  "project_id": "panw-lab-239402",
  "private_key_id": "cf06508596698639a1b065888d888b6d0422ca08",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/Cem56nreUxGQ\nRn9lQxkkpjNKbKjj22Jm2hupVzTP9Hz32L5TPLbE7Ah31GOEEx/M6CUHmjg2lVeV\nOcWCyLt0dLwXz+y7LVXSLVgGRGTWWLPgOPq/zTsxdGRBWGwR4fblPZdYFJ3K0Ca6\nUZGFn9pYSuYw1gOa3WNY8X2E+wF5sPV+L98N3YOPx2gSW25eg9gE9OysQP2MLi7J\nIaB4ogOEtCbW/ZYujuJDdHeF+Dj8GuVLoCY8fq9ayZKqPu9Iu1Vu2UAFGVRNEjDY\n0F6ieQPdLblPf6QhpYwYmwy22zPdyPDSdCT3h5k4PUezYruATe4n+LNtBhVRzpoq\nUCYhc67TAgMBAAECgf8hIf1ndHansibzRUbTFgNGV/NaKEsibOo9uS/fyHNgaqB1\nKLvZs+EyRiP+pHEEdxlzPTZiGyoLGkIWbFUIWcgpN0kBpQ42m6ZGzZZ2sv+W+jHR\n5NzLmmZDYLk1z1NVYEHYTTy/PTqHJZLFJC1MMtOrr7g8wBSsx1JztDtECESfovcW\nCLrkmuuengn1pYwZZRk12P7PUZg8aSU1lwKV2G1FV2imazIqYDcopiaNKiCX74Dp\nMTPQiNE87/nnpaWcaiiU5+eO/Ppgl1eFmyeCu+l71tXOBilo+3panJCE6KOaqh5J\nK7WbDSnE1UlQjprRVJcVRQdJHY05GHyGvlcYWUECgYEA/i8LTKX9B7rxphdXuTw6\npoOMwuu99O3Iyk3waN+T/IlAPy824cgwXSzEiewBcEeyjgrguhUQmmYvZlBHdMD6\nUZIVkDnuZGaorMq6oE+mPjXN6NHPrmWD/ml/7ALPdYJmhEcqTAGUPIhOZVWHKw6z\neMHsu8MYsYjlOQj8CWpbhoMCgYEAwGdc+8NZfNeAFks95wgYxjtgDuXofDH381tH\nA9lPr9NGeQBpCKu4k02qr1QcYlDftYsmjY5svqCu2RSkusWrR+tiUyt/e6FmhbWX\nnDV8J5G+1ygDLgreKbofDqbwTwDXVuuj0i2HJTgGyCUaTI2nGRGFjvwf6efGJ1iB\n2sNERXECgYAbk3MAX8mxuwBYapPjzrr2MbNlujmjhuCPwiDg39CoRyOnNzIXEKbe\nlOrFo8sMKVsfueJjjcF9XrSpvu/hpMYDb3vTZ9WLIvANvvi8R6fbe+7Y4VpMq0rE\noSF1s2BaeUkx9J6MHGe+oXMP31WIwFGMOk26mRHmwNlNdMITK2y+jQKBgQC+0AO8\nP5FpKUODWJ2MmVAQkGQEgmgde2Te+SAlpgfMZOiYKhsAmWUU2Uq0VONNcc1a+ySB\n8MTSDQM6kKmJ/W2PhtZdi18D2h6V7nDsX3LAv18XfDwjFm4bzdTtMAxVHY1yS4GN\neM91zumS5pD9aOJWDzV4h3yS+eRfsvwdW9hCUQKBgQDFxvIrmot6ws66zB0k6+Xf\ng8egKhM/IczAQXx/fnKKkBIHlNCfA2iqNLeG7CKS5r91d8VGB2SKtIU4dzHLoI47\n+xl/95lNWEj/eutT8ZPGvOrMBfL4tpvO5kEBjAka2PIEYTbiHTlzogZA6E7/DA0t\npQTFeFkG2vhvUFYjNk7luQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "xsoar-bigquery@panw-lab-239402.iam.gserviceaccount.com",
  "client_id": "106513437662387303346",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xsoar-bigquery%40panw-lab-239402.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
import json
data = str(json.dumps(cred))
print(repr(data))
#with open("ngu", "w") as f:
#    json.dump(cred,f)
#print(json.loads(data))