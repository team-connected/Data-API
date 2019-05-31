# Data API
## Docker Deploy
```docker run --name epd-db -p 27017:27017 -d mongo```

```docker run --name data-api -d -e conUri="mongodb:27017" -e db_name="EPD" -p 5000:5000 team-connected/data-api```

### Environment Flags
| Flag | Description |
| ------------- | ------------- |
| conUri | URI to the MongoDB Cluster Set or Host ("'mongodb://host1,host2,host3', replicaSet='rs0'" or "mongodb:27017")|
| db_name | Name of the Database to use |

## API Design
Implemented will be marked with :heavy_check_mark:

### Patient API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/patient/ | Retrieve list of patients |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/patient/[searchField]=[searchTerm] | Retrieve a patient |
| | POST | http://[hostname]/api/v1/patient/ | Create a patient |
| | PUT | http://[hostname]/api/v1/patient/email=[email] | Update a patient |
| | DELETE | http://[hostname]/api/v1/patient/email=[email] | Delete a patient |


### Metric API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/metric/email=[email] | Retrieve list of metrics of a patient |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/metric/[searchField]=[searchTerm] | Retrieve a metric |
| | POST | http://[hostname]/api/v1/metric/ | Create a metric |
| | PUT | http://[hostname]/api/v1/metric/email=[email] | Update a metric |
| | DELETE | http://[hostname]/api/v1/metric/email=[email] | Delete a metric |

### Nurse API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/nurse/ | Retrieve list of nurses |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/nurse/[searchField]=[searchTerm] | Retrieve a nurse |
| | POST | http://[hostname]/api/v1/nurse/ | Create a nurse |
| | PUT | http://[hostname]/api/v1/nurse/email=[email] | Update a nurse |
| | DELETE | http://[hostname]/api/v1/nurse/email=[email] | Delete a nurse |

### Device API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/device/ | Retrieve list of devices |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/device/[searchField]=[searchTerm] | Retrieve a device |
| | POST | http://[hostname]/api/v1/device/ | Create a device |
| | PUT | http://[hostname]/api/v1/device/email=[email] | Update a device |
| | DELETE | http://[hostname]/api/v1/device/email=[email] | Delete a device |

### Fields
#### Patient
* **_id**: Unique number
* **firstname**: Firstname
* **lastname**: Lastname
* **email**: E-Mail address
* **street**: Street name & house number
* **city**: City
* **location**: Room/Bed number
* **metrics**: List of all metrics

#### Metric
* **_id**: Unique number
* **metric_type**: Blood/Weight/Temperature?
* **timestamp**: Timestamp
* **device_id**: Device used to measure
* **nurse_id**: Nurse that measured
* **value**: List of values of the measure
* **comment**: Optional comment

#### Nurse
* **_id**: Unique number
* **firstname**: Firstname
* **lastname**: Lastname
* **email**: E-Mail address
* **depertment**: Department

#### Device
* **_id**: Unique number
* **name**: Name of the device
* **type**: Device type
* **sn**: Serialnumber
* **status**: Working/Maintenance/Unscaled
