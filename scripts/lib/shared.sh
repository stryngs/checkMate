## Check for errors and then write final status
closeOut--()
{
  ## Catch oVal
  echo $oVal > "$artifacts"

  ## Deal with errors
  if [[ $eLen -ne 0 ]]; then
      status="Open"
      echo "Error issues:" > "$eLog"
      echo "$errors" >> "$eLog"
      echo "Error issues:" >> "$artifacts"
  fi

  ## Status
  hostName=$(hostname)
  echo "$hostName:$vID:$status:$oVal:$cVal" >> "$log"
  echo -e "$vID:$status"
  echo "oVal: $oVal"
  echo -e "eLen: $eLen\n\n"
}

## Declares
cVal="** NOT USED **"
cLen="** NOT USED **"
eVal="** NOT USED **"
eLen="** NOT USED **"
oVal="** NOT USED **"
oLen="** NOT USED **"
