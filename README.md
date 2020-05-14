# FYP - SignChat Backend System
This is the SignChat Backend System. For front-end system, please see the following repository.
* [SignChat iOS App](https://github.com/eching0519/FYP-SignChat)
* [SignChat Maintenance System](https://github.com/eching0519/FYP-SignChatMaintenanceSystem)
## Installation
1. Clone the SignChat Backend System to document root directories `htdocs` of server.
   ```
   git clone https://github.com/eching0519/FYP-SignChatBackend.git
   ```
2. Update database setting in `SignChat/connection/mysqli_conn.php` and `SignChat/ai_lib/csvHandler.py`.
3. Run `SignChat/ai_lib/service.py` to start Machine Learning service.
