from unittest.mock import patch, MagicMock
from notify_function import main as notify_app

@patch("notify_function.main.bigquery.Client")
@patch("notify_function.main.LineBotApi")
def test_notify_flow(mock_line, mock_bq):
    mock_df = MagicMock()
    mock_df.groupby.return_value = {}
    mock_bq.return_value.query.return_value.to_dataframe.return_value = mock_df
    notify_app.line_bot_api = mock_line()
    notify_app.TARGET_USER_ID = "dummy"
    notify_app.run_notify()
    mock_line().push_message.assert_called()
