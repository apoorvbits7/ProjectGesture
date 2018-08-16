import predict_2 as digit_predictor
import os,sys


path = 'Digits/'

def get_digits_in_list():
    global path
    digits = []
    files = []
    for filename in os.listdir(path):
        files.append(filename)
    files.sort()
    for filename in files:
        x = digit_predictor.predict(path+filename)
        digits.append(x)
        os.remove(path+filename)
    return digits

def main():
    digits=get_digits_in_list()
    print (digits)
if __name__ == "__main__":
    main()
