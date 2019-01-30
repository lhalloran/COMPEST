/////////////////////////////////// COMPEST //////////////////////////////////////
// Landon Halloran, 2018                                                        //
// www.ljsh.ca                                                                  //
// COMPEST: Linking PEST with COMSOL to constrain DNAPL models using CSIA data. //
// Refer to journal article and supplementary info, including code on GitHub.   //
//////////////////////////////////////////////////////////////////////////////////

import com.comsol.model.Model; 
import com.comsol.model.util.ModelUtil;
import java.io.*;
import java.util.Arrays;
import java.util.*;

public class COMPEST {
	
	public static void init_params(Model model, String[] paramNames, String[] paramValues, Boolean verby) { 
	// initialize parameters that can be changed externally
		if (verby) {
			System.out.print("#COMPEST: init_params() Defining inputs: ");
			System.out.print(Arrays.toString(paramNames)+"\n");
		}
		for (int i = 0; i < paramValues.length; i++) {
			model.variable("var1").set(paramNames[i], paramValues[i]);
		}
	}
	
	public static void Array_to_CSV(double[][] data, String filename) throws IOException{
	// export 2D double array to simple .csv files - PEST .ins files should be written to tell PEST to which observation value each of values corresponds
	// this is an optional method to export to .csv format
		StringBuilder builder = new StringBuilder();
		for(int i = 0; i < data.length; i++)//for each row
		{
		   for(int j = 0; j < data[0].length; j++)//for each column
		   {
		      builder.append(data[i][j]+"");
		      if(j < data[0].length - 1) //no commas for end of row
		         builder.append(",");
		   }
		   builder.append("\n");//append new line at the end of the row
		}
		FileWriter fw = new FileWriter(filename);
		fw.write(builder.toString());
		fw.close();
	}
	
	public static void Array_to_Dat(double[][] data, String filename, Boolean verby) throws IOException{
	// export 2D double array to simple .dat files - PEST .ins files should be written to tell PEST to which observation value each of values corresponds
		if (verby) {
			System.out.println("#COMPEST: Array_to_Dat creating: "+filename);
		}
		StringBuilder builder = new StringBuilder();
		for(int i = 0; i < data.length; i++)//for each row
		{
		   for(int j = 0; j < data[0].length; j++)//for each column
		   {
		      builder.append(data[i][j]+"     \n");
		   }
		}
		FileWriter fw = new FileWriter(filename);
		fw.write(builder.toString());
		fw.close();
	}
	
	public static void main(String args[])throws Throwable {
        
		System.out.println("#COMPEST: COMPEST running...");

		/////////// READ AND DEFINE PROPERTIES //////////
//      Read parameters and paths from the property file                                      
        Properties props = new Properties();
        
//      Set the define.properties address         
        FileReader reader=new FileReader ("define.properties");        
        props.load(reader);
        
//      Read parameters from property file
        String ServerName = props.getProperty("ServerName");
        String ServerPortStr = props.getProperty("ServerPort");
        String ParamInputFile = props.getProperty("ParamInputFile");
        String ComsolFile = props.getProperty("ComsolFile");
        String ModelDataOutSuffix = props.getProperty("ModelDataOutSuffix");
		String ObservationNamesIn = props.getProperty("ObservationNames");
		String VerboseOutput = props.getProperty("VerboseOutput");
        String DataOutFolder = props.getProperty("DataOutFolder");
		
		int ServerPort = Integer.valueOf(ServerPortStr);
        String[] ObservationNames = ObservationNamesIn.split(";");
		Boolean verby = Boolean.valueOf(VerboseOutput);

		
/////////// READ FITTED PARAMETER FROM EXTERNAL FILE /////////   
        FileReader reader2 = new FileReader (ParamInputFile);			
        props.load(reader2); 
        String ParamNames=props.getProperty("ParamNames");
        String[] ParamNamesArray=ParamNames.split(";"); // Use ; as delimiter for multiple param types. This splits to string array
        String ParamUnits=props.getProperty("ParamUnits");
        String[] ParamUnitsArray=ParamUnits.split(";");
        String ParamValues=props.getProperty("ParamValues");
        String[] ParamValuesArray=ParamValues.split(";");
        String[] ParamValuesUnitsArray = new String[ParamNamesArray.length]; // for value + unit concatenation
        for (int i=0; i<ParamNamesArray.length; i++) {
        	ParamValuesUnitsArray[i]=ParamValuesArray[i]+ParamUnitsArray[i];
        	if (verby) {
			System.out.println("#COMPEST: ParamValuesUnitsArray["+i+"] = "+ParamNamesArray[i]+" = "+ParamValuesUnitsArray[i]);
			}
        }

////////////RUN COMSOL MODEL, ETC.//////////
// IMPORTANT... 
// COMSOL must be launched externally in cmd using this command or similar: 
// "C:\Program Files\COMSOL\COMSOL53\Multiphysics\bin\win64\comsolmphserver.exe" -multi on        
// (verify the path of your COMSOL Server executable)
        
//      Connect to COMSOL server:
        ModelUtil.connect(ServerName, ServerPort); 
		if (verby) {
			System.out.println("#COMPEST: CONNECTED to localhost:2036");
		}
        ModelUtil.showProgress(true); 
        
//      Load the COMSOL model file (created previously in GUI) using its directory and name it (e.g., test.mph)
        String mphFileName = ComsolFile;
        Model ModelCOMSOL = ModelUtil.load("model1d",mphFileName);	

//      Define dataset...
		if (verby) {
			System.out.println("#COMPEST: DEFINING DATASET");
		}
        ModelCOMSOL.result().numerical().create("Eval1","EvalPoint");

//		Set parameters to selected values:
        ModelCOMSOL.disableUpdates(false);
        init_params(ModelCOMSOL,ParamNamesArray,ParamValuesUnitsArray,verby);
        
//      Run the COMSOL model   
        if (verby) {
			System.out.println("#COMPEST: COMSOL Executing...");
		}
        ModelCOMSOL.sol("sol1").run();   

//		Select desired output data and positions of results, then get output data from COMSOL and export:
        double[][] COMSOLDataOut;
        String[] dtypeselect = ObservationNames;
        for(int i=0; i<dtypeselect.length; i++) { // loop through the desired parameters to output to .dat files 
            if (verby) {
				System.out.print("#COMPEST: i=" + i+". ");
			}
        	String dtypeselectNOW=dtypeselect[i];
            ModelCOMSOL.result().numerical("Eval1").set("expr", dtypeselectNOW); // select output data type
            if (verby) {
				System.out.print(dtypeselectNOW+" out. ");
			}
            ModelCOMSOL.result().numerical("Eval1").set("data", "cpt1"); // select points for output
            COMSOLDataOut = ModelCOMSOL.result().numerical("Eval1").getReal();
            if (verby) {
				System.out.print("Size: "+COMSOLDataOut.length +" x "+COMSOLDataOut[0].length+"\n");
			}
            Array_to_Dat(COMSOLDataOut,DataOutFolder+dtypeselectNOW+ModelDataOutSuffix, verby); //		Export COMSOL output to DAT
        }
        if (verby) {
			System.out.println("#COMPEST: Data outputted to folder: " + DataOutFolder);
		}

//		Disconnect from COMSOL server
        ModelUtil.disconnect();
        if (verby) {
			System.out.println("#COMPEST: DISCONNECTED FROM COMSOL SERVER.");
		}
		System.out.println("#COMPEST: COMPEST exiting...");
        System.exit(0);
        System.out.println("#COMPEST: WARNING: JAVA HAS NOT TERMINATED.");
        return;
	}
}