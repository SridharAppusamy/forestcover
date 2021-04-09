from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import pygal
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')



app = Flask(__name__)
dashboard.bind(app)
CORS(app)

best_model_Score=[.95,.98,.80,.70,1.0]
best_modelname=['KNN','XGBoost','Random Forest','SVM','Naive Bayes']

models_score=list(zip(best_modelname,best_model_Score))
print(models_score)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('Prediction.html')

@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel()
            #return Response("Prediction File created at %s!!!" % path)
        elif request.form is not None:
            path = request.form['path']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel()
            #return Response("Prediction File created at %s!!!" % path)
            bar_chart = pygal.Bar()
            bar_chart.title = 'Model comparasion'
            for i, j in models_score:
                bar_chart.add(i, j)
            barchart_data = bar_chart.render_data_uri()
            return render_template('barchart.html', barchart_data=barchart_data)

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['GET'])
@cross_origin()
def trainRouteClient():

    try:
        #if request.json['folderPath'] is not None:
            #path = request.json['folderPath']
            path = 'Training_Batch_Files'
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    app.run(port=port, debug=True)
    #host = '0.0.0.0'
    #port = 5000
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()
