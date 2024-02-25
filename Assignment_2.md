# Assignment_2

* Part 1

```
def case1(financial_data):
    # Print First 5 rows of MSFT
    # Print Last 5 rows of MSFT
    print(financial_data.head())
    print(financial_data.tail())

def case2(financial_data):
    #Resample to monthly data mean
    #Display the first 5 rows
    df = financial_data.resample("m").mean()
    print(df.head())

def case3(financial_data):
    # Create a variable daily_close and copy Adj Close from financial_data
    # Print first 20 daily returns
    daily_close = pd.DataFrame(financial_data["Adj Close"])
    daily_close["Adj Close"] = daily_close["Adj Close"].pct_change()
    print(daily_close.head(20))
    
def case4(financial_data):
    # Calculate the cumulative daily returns
    # day1 : return1  cumulative reuturn : (1+return1)-1
    # day2 : return2  cumulative reuturn : (1+return1)*(1+return2)-1
    # Print first 20 rows
    daily_close = pd.DataFrame(financial_data["Adj Close"])
    daily_close["Adj Close"] = daily_close["Adj Close"].pct_change()
    cumulative = 1
    for i in range (1,len(daily_close)):
        cumulative = cumulative * (1+daily_close["Adj Close"].iloc[i])
        daily_close["Adj Close"].iloc[i] = cumulative - 1
    print(daily_close.head(20))      

def case5(financial_data):
    # Isolate the adjusted closing prices and store it in a variable
    # Calculate the moving average for a window of 20
    # Display the last 20 moving average number
    adj_close = pd.DataFrame(financial_data["Adj Close"])
    print(adj_close.rolling(20).mean().tail(20))

def case6(financial_data):
    # Calculate the volatility for a period of 100 don't forget to multiply by square root
    # don't forget that you need to use pct_change
    # Print last 20 rows
    daily_close = pd.DataFrame(financial_data["Adj Close"])
    daily_close["Adj Close"] = daily_close["Adj Close"].pct_change()
    adj_close = pd.DataFrame(daily_close["Adj Close"])
    adj_close["Adj Close"] = adj_close["Adj Close"].rolling(100).std()
    adj_close["Adj Close"] = adj_close["Adj Close"] * np.sqrt(100)
    print(adj_close.tail(20))
```

* Part 2

```
def prepare_data(volume):
    #write your code here
    volume["Volume"] = volume["Volume"].astype(int)
    volume['Month'] = pd.to_datetime(volume['Month'])
    return volume

def check_stationarity(volume,fptr):    
    #write your code here
    ma = volume["Volume"].rolling(12).mean()
    msd = volume["Volume"].rolling(12).std()
    adtestoutput = adfuller(volume["Volume"])
    
    #don't modify the following part
    fptr.write('ADF Statistic: %f\n' % adtestoutput[0])
    fptr.write('p-value: %f\n' % adtestoutput[1])
    fptr.write('#Lags Used: %f\n' % adtestoutput[2])
    fptr.write('Number of Observation Used: %f\n' % adtestoutput[3])
    fptr.write('Critical Values:\n')
    for key, value in adtestoutput[4].items():
        fptr.write('\t%s: %f\n' % (key, value))
    return ma, msd, adtestoutput

def make_stationarity(volume,fptr):
    logvolume = np.log(volume["Volume"])
    mavolume = logvolume.rolling(12).mean()
    volume_without_trend = logvolume - mavolume 
    volume_without_trend.dropna(inplace=True) 
    adtestoutput= adfuller(volume_without_trend)
    ewma = logvolume.ewm(halflife = 12).mean()
    volume_without_trend_ewma = logvolume - ewma
    volume_without_trend_ewma.dropna(inplace=True)
    adtestoutput_ewma= adfuller(volume_without_trend_ewma)
    
    #don't modify the following part
    fptr.write('ADF test for volume_without_trend:\n')
    fptr.write('ADF Statistic: %f\n' % adtestoutput[0])
    fptr.write('p-value: %f\n' % adtestoutput[1])
    fptr.write('#Lags Used: %f\n' % adtestoutput[2])
    fptr.write('Number of Observation Used: %f\n' % adtestoutput[3])
    fptr.write('Critical Values:\n')
    for key, value in adtestoutput[4].items():
        fptr.write('\t%s: %f\n' % (key, value))
    fptr.write('\n')
    fptr.write('ADF test for ewma:\n')
    fptr.write('ADF Statistic: %f\n' % adtestoutput_ewma[0])
    fptr.write('p-value: %f\n' % adtestoutput_ewma[1])
    fptr.write('#Lags Used: %f\n' % adtestoutput_ewma[2])
    fptr.write('Number of Observation Used: %f\n' % adtestoutput_ewma[3])
    fptr.write('Critical Values:\n')
    for key, value in adtestoutput_ewma[4].items():
        fptr.write('\t%s: %f\n' % (key, value))
    return
    
def differencing(volume,fptr):
    volume_log_diff = np.log(volume["Volume"]).shift(1)
    volume_log_diff = np.log(volume["Volume"]) - volume_log_diff
    volume_log_diff.dropna(inplace=True)
    adtestoutput = adfuller(volume_log_diff)  
    
    #don't modify the following part
    fptr.write('ADF Statistic: %f\n' % adtestoutput[0])
    fptr.write('p-value: %f\n' % adtestoutput[1])
    fptr.write('#Lags Used: %f\n' % adtestoutput[2])
    fptr.write('Number of Observation Used: %f\n' % adtestoutput[3])
    fptr.write('Critical Values:\n')
    for key, value in adtestoutput[4].items():
        fptr.write('\t%s: %f\n' % (key, value))
    return    

def forecast_ts(volume):
    volume_log_diff = np.log(volume["Volume"]).shift(1)
    volume_log_diff = np.log(volume["Volume"]) - volume_log_diff
    volume_log_diff.dropna(inplace=True)
    ACF = acf(volume_log_diff)
    model = ARIMA(volume_log_diff,order=(2,1,2))
    results_ARIMA = model.fit()
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    predictions_ARIMA = predictions_ARIMA_diff + np.log(volume["Volume"]).shift(1).dropna()
    predictions_ARIMA_initial = np.exp(predictions_ARIMA) 
    return ACF,predictions_ARIMA_diff,predictions_ARIMA_diff_cumsum,predictions_ARIMA_initial
```

* Part 3

```
def transaction(seb, nic):
    global bank_account
    global seb_thread_acq
    global nic_thread_acq
    global var_lock
    global current_thread
    
    seb_runs = seb
    nic_runs = nic
    
    while seb_runs > 0 or nic_runs > 0:
        if seb_thread_acq == False and nic_thread_acq == False:        
            current_thread = run_thread(seb_runs, nic_runs)
        
        var_status = thread_acquire_var(current_thread)       
        if var_status == "Locked":
            continue
        if current_thread == "Seb":
            if seb_thread_acq == False:
                seb_runs += seb_thread()
                seb_thread_acq = True
                continue
            else:
                update_thread()
                seb_thread_acq = False
                seb_runs -= 1          
        else:
            if nic_thread_acq == False:
                nic_runs += nic_thread()
                nic_thread_acq = True
                continue
            else:
                update_thread()
                nic_thread_acq = False
                nic_runs -= 1
    return bank_account
```

* Part 4

```
class OperatorNotRecognizedError(Exception):
    pass

class NegativeInputError(Exception):
    pass

class NegativeOutputError(Exception):
    pass

class NonIntegerInputError(Exception):
    pass

class OutputTooLargeError(Exception):
    pass
    
class ValueError(Exception):
    pass

def pocket_calculator(x, operator, y):
    # Write your code here JUST DO IT!
    try:
        if not (x.replace("-","").replace(".","").isnumeric()) or not (y.replace("-","").replace(".","").isnumeric()):
            raise ValueError   
        if operator not in ["+","-","x","/"]:
            raise OperatorNotRecognizedError
        if operator == "x":
            operator = "*"  
        if "." in x or "." in y:
            raise NonIntegerInputError
        if float(y) == 0:
            return "0"    
        if int(x) < 0 or int(y) < 0:
            raise NegativeInputError
        if eval(x+operator+y) < 0:
            raise NegativeOutputError
        if eval(x+operator+y) > 9999999:
            raise OutputTooLargeError
        
    except OperatorNotRecognizedError:
        return 'OperatorNotRecognized'
    
    except ValueError:
        return 'InputNotANumber'

    except NegativeInputError:
        return 'NegativeInput'
        
    except NegativeOutputError:
        return 'NegativeOutput'
        
    except NonIntegerInputError:
        return 'NonIntegerInput'
        
    except OutputTooLargeError:
        return 'OutputTooLarge'
    result = str(int(eval(x+operator+y)))
    return result
```