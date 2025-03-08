#!/bin/bash

curl 'http://localhost:8000/api/submit-preferences' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'session=eyJfc3RhdGVfbWljcm9zb2Z0X2tiWFR3RFdXVWl3UWtHY242MEhYaFlhNURZOTc4byI6IHsiZGF0YSI6IHsicmVkaXJlY3RfdXJpIjogImh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hdXRoL2NhbGxiYWNrIiwgIm5vbmNlIjogIlJ4ODRWUktGa1RWNm43blJ1Z2tZIiwgInVybCI6ICJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vY29tbW9uL29hdXRoMi92Mi4wL2F1dGhvcml6ZT9yZXNwb25zZV90eXBlPWNvZGUmY2xpZW50X2lkPXlvdXItbWljcm9zb2Z0LWNsaWVudC1pZCZyZWRpcmVjdF91cmk9aHR0cCUzQSUyRiUyRmxvY2FsaG9zdCUzQTgwMDAlMkZhdXRoJTJGY2FsbGJhY2smc2NvcGU9b3BlbmlkK3Byb2ZpbGUrZW1haWwmc3RhdGU9a2JYVHdEV1dVaXdRa0djbjYwSFhoWWE1RFk5NzhvJm5vbmNlPVJ4ODRWUktGa1RWNm43blJ1Z2tZIn0sICJleHAiOiAxNzQxMzA5Njk0LjczMjQyNzh9LCAidXNlciI6IHsib2lkIjogIjhjM2EwMzAzLWYwMzAtNDllMi05NGI2LWY4OWI5Nzc3NjRkMCIsICJzdWIiOiAiOGMzYTAzMDMtZjAzMC00OWUyLTk0YjYtZjg5Yjk3Nzc2NGQwIiwgInRpZCI6ICJmYWtlLXRlbmFudC1pZC0xMjM0NSIsICJ1cG4iOiAiQWxpY2VAdXRzLmNvbSIsICJwcmVmZXJyZWRfdXNlcm5hbWUiOiAiQWxpY2VAdXRzLmNvbSIsICJuYW1lIjogIkFsaWNlIiwgImVtYWlsIjogIkFsaWNlQHV0cy5jb20iLCAiZ2l2ZW5fbmFtZSI6ICJBbGljZSIsICJmYW1pbHlfbmFtZSI6ICIiLCAiYXVkIjogImZha2UtY2xpZW50LWlkLTEyMzQ1IiwgImlzcyI6ICJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vZmFrZS10ZW5hbnQtaWQvdjIuMCIsICJpYXQiOiAxNzQxMzkyOTE5LCAiZXhwIjogMTc0MTM5NjUxOSwgIm5iZiI6IDE3NDEzOTI5MTksICJyb2xlcyI6IFsiVXNlciJdfX0=.Z8uMFw.Z4SmltJGiGCCnDOivMqSpxOhm4k' \
  -H 'Origin: http://localhost:8000' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://localhost:8000/form.html' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"preferences":[{"project_id":1009,"strength":1},{"project_id":1005,"strength":0.9},{"project_id":1001,"strength":0.8},{"project_id":1002,"strength":0.7},{"project_id":1003,"strength":0.6},{"project_id":1007,"strength":0.5},{"project_id":1006,"strength":0.4},{"project_id":1008,"strength":0.3},{"project_id":1010,"strength":0.2},{"project_id":1004,"strength":0.1}],"will_sign_contract":false}'

curl 'http://localhost:8000/api/submit-preferences' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'session=eyJfc3RhdGVfbWljcm9zb2Z0X2tiWFR3RFdXVWl3UWtHY242MEhYaFlhNURZOTc4byI6IHsiZGF0YSI6IHsicmVkaXJlY3RfdXJpIjogImh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hdXRoL2NhbGxiYWNrIiwgIm5vbmNlIjogIlJ4ODRWUktGa1RWNm43blJ1Z2tZIiwgInVybCI6ICJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vY29tbW9uL29hdXRoMi92Mi4wL2F1dGhvcml6ZT9yZXNwb25zZV90eXBlPWNvZGUmY2xpZW50X2lkPXlvdXItbWljcm9zb2Z0LWNsaWVudC1pZCZyZWRpcmVjdF91cmk9aHR0cCUzQSUyRiUyRmxvY2FsaG9zdCUzQTgwMDAlMkZhdXRoJTJGY2FsbGJhY2smc2NvcGU9b3BlbmlkK3Byb2ZpbGUrZW1haWwmc3RhdGU9a2JYVHdEV1dVaXdRa0djbjYwSFhoWWE1RFk5NzhvJm5vbmNlPVJ4ODRWUktGa1RWNm43blJ1Z2tZIn0sICJleHAiOiAxNzQxMzA5Njk0LjczMjQyNzh9LCAidXNlciI6IHsib2lkIjogIjFkMDY0ZTE1LTYyOTMtNGQ4Yy05NTMxLTE5NmVjZWE5ZjlmYiIsICJzdWIiOiAiMWQwNjRlMTUtNjI5My00ZDhjLTk1MzEtMTk2ZWNlYTlmOWZiIiwgInRpZCI6ICJmYWtlLXRlbmFudC1pZC0xMjM0NSIsICJ1cG4iOiAiQm9iQHV0cy5jb20iLCAicHJlZmVycmVkX3VzZXJuYW1lIjogIkJvYkB1dHMuY29tIiwgIm5hbWUiOiAiQm9iIiwgImVtYWlsIjogIkJvYkB1dHMuY29tIiwgImdpdmVuX25hbWUiOiAiQm9iIiwgImZhbWlseV9uYW1lIjogIiIsICJhdWQiOiAiZmFrZS1jbGllbnQtaWQtMTIzNDUiLCAiaXNzIjogImh0dHBzOi8vbG9naW4ubWljcm9zb2Z0b25saW5lLmNvbS9mYWtlLXRlbmFudC1pZC92Mi4wIiwgImlhdCI6IDE3NDEzOTI5NTQsICJleHAiOiAxNzQxMzk2NTU0LCAibmJmIjogMTc0MTM5Mjk1NCwgInJvbGVzIjogWyJVc2VyIl19fQ==.Z8uMOg.HRGPrFiuWz2iFt0DxKGzBb22lSE' \
  -H 'Origin: http://localhost:8000' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://localhost:8000/form.html' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"preferences":[{"project_id":1010,"strength":1},{"project_id":1001,"strength":0.9},{"project_id":1003,"strength":0.8},{"project_id":1004,"strength":0.7},{"project_id":1005,"strength":0.6},{"project_id":1006,"strength":0.5},{"project_id":1007,"strength":0.4},{"project_id":1008,"strength":0.3},{"project_id":1002,"strength":0.2},{"project_id":1009,"strength":0.1}],"will_sign_contract":true}'

curl 'http://localhost:8000/api/submit-preferences' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -b 'session=eyJfc3RhdGVfbWljcm9zb2Z0X2tiWFR3RFdXVWl3UWtHY242MEhYaFlhNURZOTc4byI6IHsiZGF0YSI6IHsicmVkaXJlY3RfdXJpIjogImh0dHA6Ly9sb2NhbGhvc3Q6ODAwMC9hdXRoL2NhbGxiYWNrIiwgIm5vbmNlIjogIlJ4ODRWUktGa1RWNm43blJ1Z2tZIiwgInVybCI6ICJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vY29tbW9uL29hdXRoMi92Mi4wL2F1dGhvcml6ZT9yZXNwb25zZV90eXBlPWNvZGUmY2xpZW50X2lkPXlvdXItbWljcm9zb2Z0LWNsaWVudC1pZCZyZWRpcmVjdF91cmk9aHR0cCUzQSUyRiUyRmxvY2FsaG9zdCUzQTgwMDAlMkZhdXRoJTJGY2FsbGJhY2smc2NvcGU9b3BlbmlkK3Byb2ZpbGUrZW1haWwmc3RhdGU9a2JYVHdEV1dVaXdRa0djbjYwSFhoWWE1RFk5NzhvJm5vbmNlPVJ4ODRWUktGa1RWNm43blJ1Z2tZIn0sICJleHAiOiAxNzQxMzA5Njk0LjczMjQyNzh9LCAidXNlciI6IHsib2lkIjogIjQyNWExNTMwLTdhZDctNDc4Ny04YjcyLWMxMGI0YzMyNGVmNCIsICJzdWIiOiAiNDI1YTE1MzAtN2FkNy00Nzg3LThiNzItYzEwYjRjMzI0ZWY0IiwgInRpZCI6ICJmYWtlLXRlbmFudC1pZC0xMjM0NSIsICJ1cG4iOiAiQ2hhcmxpZUB1dHMuY29tIiwgInByZWZlcnJlZF91c2VybmFtZSI6ICJDaGFybGllQHV0cy5jb20iLCAibmFtZSI6ICJDaGFybGllIiwgImVtYWlsIjogIkNoYXJsaWVAdXRzLmNvbSIsICJnaXZlbl9uYW1lIjogIkNoYXJsaWUiLCAiZmFtaWx5X25hbWUiOiAiIiwgImF1ZCI6ICJmYWtlLWNsaWVudC1pZC0xMjM0NSIsICJpc3MiOiAiaHR0cHM6Ly9sb2dpbi5taWNyb3NvZnRvbmxpbmUuY29tL2Zha2UtdGVuYW50LWlkL3YyLjAiLCAiaWF0IjogMTc0MTM5Mjk3OSwgImV4cCI6IDE3NDEzOTY1NzksICJuYmYiOiAxNzQxMzkyOTc5LCAicm9sZXMiOiBbIlVzZXIiXX19.Z8uMUw.bH4bRoWWAtD-2dPVlPhyywJGlQM' \
  -H 'Origin: http://localhost:8000' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://localhost:8000/form.html' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"preferences":[{"project_id":1001,"strength":1},{"project_id":1002,"strength":0.9},{"project_id":1010,"strength":0.8},{"project_id":1003,"strength":0.7},{"project_id":1009,"strength":0.6},{"project_id":1006,"strength":0.5},{"project_id":1007,"strength":0.4},{"project_id":1004,"strength":0.3},{"project_id":1008,"strength":0.2},{"project_id":1005,"strength":0.1}],"will_sign_contract":true}'