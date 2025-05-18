from unittest.mock import patch, MagicMock
import pandas as pd
from fetch_function import main as fetch_app

@patch("fetch_function.main.bigquery.Client")
def test_save(mock_bq):
    mock_client = MagicMock()
    mock_bq.return_value = mock_client
    mock_client.load_table_from_dataframe.return_value.result.return_value = None
    df = pd.DataFrame({"Open": [1], "High": [2], "Low": [0], "Close": [1], "Volume": [100], "symbol": ["0000.T"], "date": ["2025-01-01"]})
    fetch_app.save_to_bigquery(df)
    mock_client.load_table_from_dataframe.assert_called_once()
