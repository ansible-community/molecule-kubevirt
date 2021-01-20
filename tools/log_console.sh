#!/bin/bash
# Backgroung wait for Pod reflecting VM to be reday then log console
while true; do
  until kubectl wait --for=condition=Ready pod -l kubevirt.io=virt-launcher --namespace default;
    do echo "Still Waiting Pod to start..."; sleep 5;
  done

  LOGFILE="virtcl-console-$(date '+%Y-%m-%d-%H-%M-%S').log"
  echo "Starting virtctl console" >> /tmp/${LOGFILE}
  sudo script -e -c "virtctl console instance" >> /tmp/${LOGFILE}
done
