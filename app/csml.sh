# bash file to execute CSML

# for training classifier and inferring images.
python src/main.py -t "train" -l "label" -o "result" -m "model.pkl" -i "infer"

# for only inferring images.
#python src/main.py -f -i "infer" -o "result" -m "model.pkl"
