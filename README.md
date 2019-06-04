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
| :heavy_check_mark: | GET | http://[hostname]/api/v1/patient | Retrieve list of patients |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/patient/[searchField]=[searchTerm] | Retrieve a patient |
| :heavy_check_mark: | POST | http://[hostname]/api/v1/patient | Create a patient |
| :heavy_check_mark: | PUT | http://[hostname]/api/v1/patient/email=[email] | Update a patient |
| :heavy_check_mark: | DELETE | http://[hostname]/api/v1/patient/email=[email] | Delete a patient |


### Metric API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/metric/email=[email] | Retrieve list of metrics of a patient |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/metric/[searchField]=[searchTerm] | Retrieve a metric |
| :heavy_check_mark: | POST | http://[hostname]/api/v1/metric/email=[email] | Create a metric |
| :heavy_check_mark: | PUT | http://[hostname]/api/v1/metric/id=[id] | Update a metric |
| :heavy_check_mark: | DELETE | http://[hostname]/api/v1/metric/id=[id] | Delete a metric |

### Nurse API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/nurse | Retrieve list of nurses |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/nurse/[searchField]=[searchTerm] | Retrieve a nurse |
| :heavy_check_mark: | POST | http://[hostname]/api/v1/nurse | Create a nurse |
| :heavy_check_mark: | PUT | http://[hostname]/api/v1/nurse/email=[email] | Update a nurse |
| :heavy_check_mark: | DELETE | http://[hostname]/api/v1/nurse/email=[email] | Delete a nurse |

### Device API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/device | Retrieve list of devices |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/device/[searchField]=[searchTerm] | Retrieve a device |
| :heavy_check_mark: | POST | http://[hostname]/api/v1/device | Create a device |
| :heavy_check_mark: | PUT | http://[hostname]/api/v1/device/sn=[serialNumber] | Update a device |
| :heavy_check_mark: | DELETE | http://[hostname]/api/v1/device/sn=[serialNumber] | Delete a device |

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
* **department**: Department

#### Device
* **_id**: Unique number
* **name**: Name of the device
* **type**: Device type
* **sn**: Serialnumber
* **status**: Working/Maintenance/Unscaled
