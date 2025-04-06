FROM python
WORKDIR /APP
COPY . /APP
RUN pip install update
RUN pip install -r requirements.txt

ENV T_ACCESS_TOKEN = 7413461681:AAGEpXSdJHZWAKIHUTDQb3PU3Jw02ujpW74
ENV C_ACCESS_TOKEN=9d5b8dd5-76e6-4b12-b92e-cb4e2061f27b
ENV T_LINK = t.me/jonascc_bot
ENV FIREBASE_CREDENTIALS = ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAidGVsZWdyYW1ib3QtMzViNTEiLAogICJwcml2YXRlX2tleV9pZCI6ICIwNGYwYzE2MWYxMGM2YmQ5ODI4MWE1MDI4M2MyYzUwMmY0YzZlOGU5IiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUUNmVmVJNks3ekh6YWxjXG4vczNKSHBsLzNCVk5iNVNzOXZzSXA1anlNa1h5amFjNjNjcXhNdFRFSE8xeWFCNG1yblRtL09BbWxRdnE5YnRnXG4xWHFWdTZWeFljbTFXZFRrUW9MYVQxRWlrcWNDUUhZZGJKdHdwU0tXaVR0V2M3dEg0UGI1NHRCeVIxM09Vd1hwXG42alI4REcreTNoUTlicThlNVVhZTlBa0pDa0dMODNQUzRjL0tCbzRnd3p6M25QWjdaQm5leEJsMy80MVNIcTcvXG5MN0RGQUNwTGl0cFpON3A1dFVhY3ZUZXp6YVRhc3hQaUtkZ1JSQTVSaEYyNnJ6VHJhMFdaM1VlanJ1dTRpWXd5XG5SZzF0L0hkeHlrTFFaVjJpdkhpYkhQRGhpMTBxMFR4eHVkTEdyYmhQcjNKNTdzc3JnUk5UaThyaXZNUi9GMEM5XG4zaklhR1FVdEFnTUJBQUVDZ2dFQUUzOUxhUW5jRm1qOHJnUUNBM2ZLbWNKQkd4SXAwOFovTG01dndVZFVsdHN0XG5tUDcxNUJ3UHZCVzhHcEZTQ3pLeTNHY2FPSzVwWUcyRWFkT0ZwaGZwcFVldGlwTDlBWmQvOHAzZEZFbDB4VXBGXG5DZEcxN2FGUGE3Tk1Qd1ozWnRMSTlnZ0NzTkU1MGRzSDhMazNoZXh4cUtZVFBQY3oxNmgvclVpNGFGSklkZ3I1XG5TdHRPeWluOTlPUWlIdkdxZjhUUkh4c3FSVlZqTTZCRVAzaWtwRlluWk9CTEMxY2dieFZjRjVpbE9iMmlKVjBLXG5peS9VRWJIK1NhUngyWDFXMEIzSE9ieDFBRURSWUFUYlFDTE94TDIrWW9nNXNSUis4MUI5UW5EcHQ1ZkNVTk9ZXG5oT01meEJiamdnWDh6WTN2Y2psbm1CNUJiZXh5alRWa1NvZFZBb2o4SXdLQmdRRGJaazJBK1pEd1ZkUGtZT0hnXG5QVGg0OXREUFNaUEV0Z3Vmb21DeTFzVFVZZmt4MnVQZmJyNU5YRXNIbGFlZDVtUnozNEU4VWVFS3BvTG41QUVOXG5MQVkvdXA1ZzdDTHVjUXdRcEJQZ2lrRG0waUN6M1VjdEYzNHdseXJETDNPSERCRjkxV1ZEd09QbHJLTHpBSFU3XG5qQkxFZW1KUEdpY25VWDlYSTRMZmpwRVNEd0tCZ1FDNTZub3N4U3A3MExYQ0RxYy93bjVvQWRpWFBkV2F4TnNtXG4va3BhQXNPbTVlUlcxUTRBU2hERzhadExJS2l3TkxSRXJIa0pRWVA5a1FlUzI2TmZNcW1wSXp2dzNJenBPS3UrXG55S2pkZHpKa0tjay8veEVadmRlRmU5c3dnVEJuU0pYNnRHazVNV2UwODd0NEVUV1pRaGhkQVVzRUtsV0g3Y3g0XG43NllkYWpCQkF3S0JnUUNXcHB1bmFUYWQ0TUZidXk2K2RDczMzSHFySzJHZEhFZkUrSkdmbTV1U0hpZ25sSjhPXG5DQlFDT05LSVJiblAwYWkrYkFWb3J1eHhETDhzamNJdkVrREVOOWVTdy9LRWVmbUgzN0tLWjBTRGVsdmNSYUFmXG5GVmVmODl6NEk3Z1hUakVnajR3MlJ0ZjJHR0hYckVQVGZLNVNYWnJ0cUE2a2ovQjVuRGU4WEQrKy93S0JnRlMxXG5CTjJKS0FZcDNlYUJEcXI2VHVYTWtZYTNZYStXcWRObVlUSUp1R00rczM3c3EraHQxcDhPVGhjNDFpTVNvRi81XG54VnYyUWRFeVZ5VU9kYTFXUS84UVVxczNrZXhoS2I5UFpjRWlJZytKQ216aUprUjRQczVPMUZ1UlFTQ043ZWZBXG5jNERmaGNUb21DM29pV2MrdWlNR0I4dnFEZlpVM3FqclorQlhGWTFKQW9HQU1IcjR3RjVXeUVYdmJyNVhSak5HXG5RMnp6MDk4S0FaTnNaSmJRcWswdmYrS1JOTGRQaDNQV1VRVjNaTmkxS3VTS3lBb21FOUtRYzJlM01ia1NGUFZvXG5UV2ZrZnc3cmZHWEswaTQzS2lRanlFK2FWMVJBajdKeXZSWVJLUkZlOXAxVk1SdzJFSUFwbkRTSGs5d3l3YnZQXG5xRUdGSk90aTRnaEljdlpXVTVVOVl4cz1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsCiAgImNsaWVudF9lbWFpbCI6ICJmaXJlYmFzZS1hZG1pbnNkay1mYnN2Y0B0ZWxlZ3JhbWJvdC0zNWI1MS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgImNsaWVudF9pZCI6ICIxMDkzOTYzNjU3NDc0ODk5NDYwMTIiLAogICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsCiAgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsCiAgImF1dGhfcHJvdmlkZXJfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMiLAogICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L2ZpcmViYXNlLWFkbWluc2RrLWZic3ZjJTQwdGVsZWdyYW1ib3QtMzViNTEuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20iCn0K

CMD python chatbot.py