'''
@author: Yannis Papadopoulos, Shahn Nadeau
'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QRadioButton
from PyQt5.QtCore import *
import pandas as pd
from scipy import stats
from imageio.plugins._tifffile import askopenfilename
from PyQt5.Qt import QButtonGroup, QLabel
        
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyProject'
        self.left = 550
        self.top = 350
        self.width = 625
        self.height = 200
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        fileButton = QPushButton('Select a DataSet', self)
        fileButton.move(60,30) 
        fileButton.clicked.connect(self.getfile)
        self.applyButton = QPushButton('Apply Tests', self)
        self.applyButton.move(215,30) 
        self.applyButton.clicked.connect(self.newWindow)
        self.applyButton.setEnabled(False)
        
        self.displayText = QLabel("", self)
        self.displayText.move(375,0)
        self.displayText.setFixedHeight(150)
        self.displayText.setFixedWidth(250)
        self.displayText.setAlignment(Qt.AlignTop)
        self.displayText.setAlignment(Qt.AlignLeft)
        self.displayText.setWordWrap(True)
        self.displayText.setAutoFillBackground(True);
        self.displayText.setStyleSheet("QLabel { background-color: rgba(169,169,169); }")
        
        self.displayResult = QLabel("", self)
        self.displayResult.move(375,155)
        self.displayResult.setFixedHeight(200)
        self.displayResult.setFixedWidth(250)
        self.displayResult.setAlignment(Qt.AlignTop)
        self.displayResult.setAlignment(Qt.AlignLeft)
        self.displayResult.setWordWrap(True)
        self.displayResult.setAutoFillBackground(True);
        self.displayResult.setStyleSheet("QLabel { background-color: rgba(169,169,169); }")
        
        paraNonPara = QButtonGroup(self)
        anovaPara = QButtonGroup(self)
        pairUnPair = QButtonGroup(self)
        studentAnova = QButtonGroup(self)
        
        self.anova = QRadioButton('Anova',self)
        self.anova.move(250,90)
        self.anova.setChecked(False)
        self.student = QRadioButton('Student-T',self)
        self.student.move(60,90)
        self.student.setChecked(False)
        studentAnova.addButton(self.anova)
        studentAnova.addButton(self.student)
        
        self.stuPara = QRadioButton('Parametric',self)
        self.stuPara.move(10,120)
        self.stuPara.setChecked(False)
        self.stuNonpara = QRadioButton('non-Parametric',self)
        self.stuNonpara.move(10,150)
        self.stuNonpara.setChecked(False)
        paraNonPara.addButton(self.stuPara)
        paraNonPara.addButton(self.stuNonpara)
        
        self.anoPara = QRadioButton('Parametric',self)
        self.anoPara.move(250,120)
        self.anoPara.setChecked(False)
        self.anoNonpara = QRadioButton('non-Parametric',self)
        self.anoNonpara.move(250,150)
        self.anoNonpara.setChecked(False)
        anovaPara.addButton(self.anoPara)
        anovaPara.addButton(self.anoNonpara)
        
        self.pair = QRadioButton('Paired',self)
        self.pair.move(130,120)
        self.pair.setChecked(False)
        self.unPair = QRadioButton('Unpaired',self)
        self.unPair.move(130,150)
        self.unPair.setChecked(False)
        pairUnPair.addButton(self.pair)
        pairUnPair.addButton(self.unPair)
        
        self.pair.setEnabled(False)
        self.unPair.setEnabled(False)
        self.anoPara.setEnabled(False)
        self.anoNonpara.setEnabled(False)
        self.stuPara.setEnabled(False)
        self.stuNonpara.setEnabled(False)
        self.anova.setEnabled(False)
        self.student.setEnabled(False)
    
    def newWindow(self):
        if (self.student.isChecked()):
            #para=student t, non-para-paird=signrank, non-para-unpaird=ranksum
            if(self.stuPara.isChecked()):
                if (self.pair.isChecked()):
                    self.displayResult.setText(stats.ttest_rel(df.iloc[:,0], df.iloc[:,1]).__str__())
                else:
                    self.displayResult.setText(stats.ttest_ind(df.iloc[:,0], df.iloc[:,1], equal_var=False).__str__())
            else:
                if (self.pair.isChecked()):
                    self.displayResult.setText(stats.wilcoxon(df.iloc[:,0], df.iloc[:,1], zero_method='wilcox', correction=False).__str__())
                else:
                    self.displayResult.setText(stats.ranksums(df.iloc[:,0], df.iloc[:,1]).__str__())
        if (self.anova.isChecked()):
            #para=anova, non-para=kruskalwallis
            #pca reduce to 3 or 2
            if(self.anoPara.isChecked()):
                self.displayResult.setText(stats.f_oneway(df.iloc[:,0],df.iloc[:,1],df.iloc[:,2]).__str__())
            else:
                self.displayResult.setText(stats.kruskal(df.iloc[:,0],df.iloc[:,1],df.iloc[:,2]).__str__())

    def getfile(self):
        #get the file name and if it is not empty do stuff
        filename = askopenfilename()
        if (filename != ''):
            #check that it is an xlsx file
            if (filename.endswith('.xlsx')):
                xls_file = pd.ExcelFile(filename)
                sheetName = xls_file.sheet_names
                tempParse = xls_file.parse(sheetName[0])
                tempParse = tempParse.dropna(axis=1,how='all')
                #if the data set is empty
                if (len(tempParse.columns) == 0):
                    self.displayText.setText("DataSet is Empty!")
                    self.displayResult.setText("")
                    self.applyButton.setEnabled(False)
                    self.pair.setEnabled(False)
                    self.unPair.setEnabled(False)
                    self.anoPara.setEnabled(False)
                    self.anoNonpara.setEnabled(False)
                    self.stuPara.setEnabled(False)
                    self.stuNonpara.setEnabled(False)
                    self.anova.setEnabled(False)
                    self.student.setEnabled(False)
                    return
                if (len(tempParse.columns) > 3):
                    self.displayText.setText("DataSet is too Large!")
                    self.displayResult.setText("")
                    self.applyButton.setEnabled(False)
                    self.pair.setEnabled(False)
                    self.unPair.setEnabled(False)
                    self.anoPara.setEnabled(False)
                    self.anoNonpara.setEnabled(False)
                    self.stuPara.setEnabled(False)
                    self.stuNonpara.setEnabled(False)
                    self.anova.setEnabled(False)
                    self.student.setEnabled(False)
                    return
                tempParse = list(tempParse)                  
                global df
                #use tempParse to check if file had headers
                if(isinstance(tempParse[0],float) or isinstance(tempParse[0],int)):
                    df = xls_file.parse(sheetName[0], header = None)
                else:
                    df = xls_file.parse(sheetName[0])
                #cut the NaN columns out
                df = df.dropna(axis=1,how='all')
                #cut any NaN values out
                df = df.dropna()
                #activate the buttons and radio buttons depending on your data set
                self.displayText.setText(df.describe(include = 'all').to_string())
                self.displayResult.setText("")
                if (len(df.columns) == 1):
                    self.applyButton.setEnabled(False)
                    self.student.setEnabled(False)
                    self.student.setChecked(False)
                    self.pair.setEnabled(False)
                    self.pair.setChecked(False)
                    self.unPair.setEnabled(False)
                    self.stuPara.setEnabled(False)
                    self.stuPara.setChecked(False)
                    self.stuNonpara.setEnabled(False)
                    self.anova.setEnabled(False)
                    self.anoPara.setEnabled(False)
                    self.anoNonpara.setEnabled(False)
                elif (len(df.columns) == 2):
                    self.applyButton.setEnabled(True)
                    self.student.setEnabled(True)
                    self.student.setChecked(True)
                    self.pair.setEnabled(True)
                    self.pair.setChecked(True)
                    self.unPair.setEnabled(True)
                    self.stuPara.setEnabled(True)
                    self.stuPara.setChecked(True)
                    self.stuNonpara.setEnabled(True)
                    self.anova.setEnabled(False)
                    self.anoPara.setEnabled(False)
                    self.anoNonpara.setEnabled(False)
                else:
                    self.applyButton.setEnabled(True)
                    self.anova.setEnabled(True)
                    self.anova.setChecked(True)
                    self.anoPara.setEnabled(True)
                    self.anoPara.setChecked(True)
                    self.anoNonpara.setEnabled(True)
                    self.student.setEnabled(False)
                    self.pair.setEnabled(False)
                    self.unPair.setEnabled(False)
                    self.stuPara.setEnabled(False)
                    self.stuNonpara.setEnabled(False)
            else:
                #need warning for wrong file type
                self.displayText.setText("Wrong file type")
                self.displayResult.setText("")
                self.applyButton.setEnabled(False)
                self.pair.setEnabled(False)
                self.unPair.setEnabled(False)
                self.anoPara.setEnabled(False)
                self.anoNonpara.setEnabled(False)
                self.stuPara.setEnabled(False)
                self.stuNonpara.setEnabled(False)
                self.anova.setEnabled(False)
                self.student.setEnabled(False)
        else:
            #need warning for no file chosen
            self.displayText.setText("No file selected")
            self.displayResult.setText("")
            self.applyButton.setEnabled(False)
            self.pair.setEnabled(False)
            self.unPair.setEnabled(False)
            self.anoPara.setEnabled(False)
            self.anoNonpara.setEnabled(False)
            self.stuPara.setEnabled(False)
            self.stuNonpara.setEnabled(False)
            self.anova.setEnabled(False)
            self.student.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())