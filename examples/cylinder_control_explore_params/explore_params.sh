#!/bin/bash

if [ $# -ne 0 ]; then
   echo "Execution: ./explore_parameters.sh"
   exit
fi

WORK_FOLDER=$PWD
SIM_TEMPLATE_FOLDER=$WORK_FOLDER/../cylinder_control
EXEC_FOLDER=$WORK_FOLDER/tmp
DATA_FOLDER=$WORK_FOLDER/explore


KPROP_LIST="0.001 0.005 0.010 0.050 0.100 0.500"
KINT_LIST="0.001 0.005 0.010 0.050 0.100 0.500"
echo "Running Simulation..."

for KPROP in  ${KPROP_LIST}; do
   for KINT in  ${KINT_LIST}; do
       cd $WORK_FOLDER
       DATA_FOLDER_SIM="$DATA_FOLDER/cylinder_control_kprop_${KPROP}_kint_${KINT}"
       if [ ! -d "$DATA_FOLDER_SIM" ]; then
         rm -rf $EXEC_FOLDER/
         mkdir -p $EXEC_FOLDER
         cp -r $SIM_TEMPLATE_FOLDER/* $EXEC_FOLDER
         cd $EXEC_FOLDER
         echo "Running cylinder control at: ${EXEC_FOLDER}..."
         sed -i "s/kProp *=.*/kProp = ${KPROP}/g" python/user/controller.py
         sed -i "s/kInt *=.*/kInt = ${KINT}/g" python/user/controller.py
         ./exec_simulation.sh 2>log.txt
         EXEC_RESULT=$?
          if [ $EXEC_RESULT -eq 0 ]; then
            echo "Finished cylinder control. Collecting results..."
            mkdir -p $DATA_FOLDER_SIM
            cp results/*.dat results/*.txt $DATA_FOLDER_SIM
          else
            echo "ERROR DETECTED. SKIPPING..."
          fi
       fi
   done
done

