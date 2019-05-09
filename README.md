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
| | GET | http://[hostname]/api/v1/users/ | Retrieve list of users |

### Metric API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| | GET | http://[hostname]/api/v1/workouts/email=[email] | Retrieve a list of workouts from a user |

### Nurse API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/videos/ | Retrieve list of videos |

### Device API
| Implemented | HTTP Method | URL | Action |
| ------------- | ------------- | ------------- | ------------- |
| :heavy_check_mark: | GET | http://[hostname]/api/v1/videos/ | Retrieve list of videos |

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
