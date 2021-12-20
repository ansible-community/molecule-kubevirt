#!/bin/bash
# Backgroung wait for Pod reflecting VM to be reday then log console
until kubectl wait --for=condition=Ready pod -l kubevirt.io=virt-launcher --namespace default 2> /dev/null;
  do echo "Still Waiting VM Pod to be in ready condition"; sleep 30;
done

LOGFILE="virtcl-console-$(date '+%Y-%m-%d-%H-%M-%S').log"
echo "Starting virtctl console" >> ${LOG_DIR}/${LOGFILE}
script -e -c "virtctl console instance" >> ${LOG_DIR}/${LOGFILE}
