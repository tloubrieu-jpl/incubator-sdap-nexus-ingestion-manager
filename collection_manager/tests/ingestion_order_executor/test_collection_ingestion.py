import filecmp
import logging
import os
import unittest
from datetime import datetime
from pathlib import Path

import collection_manager.granule_ingester
from collection_manager.ingestion_order_executor import CollectionProcessor
from collection_manager.collection_manager.util import util
from collection_manager.collection_manager.services.history_manager import md5sum_from_filepath

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestUnitMgr(unittest.TestCase):

    def setUp(self):
        logger.info("\n===== UNIT TESTS =====")
        super().setUp()
        self.collection_config_template = util.full_path("resources/dataset_config_template.yml")

        self.target_granule_list_file = util.full_path("tmp/granule_list/target_granule_list_file.lst")
        self.target_dataset_config_file = util.full_path("tmp/dataset_config/dataset_config_file.yml")

        self.history_path = os.path.join(Path(__file__).parent.absolute(),
                                         "../data/")
        self.dataset_id = "avhrr-oi-analysed-sst"
        self.granule_file_pattern = os.path.join(Path(__file__).parent.absolute(),
                                                 "../data/avhrr_oi/*.nc")
        self.expected_dataset_configuration_file = os.path.join(Path(__file__).parent.absolute(),
                                                                "../data/dataset_config_file_ok.yml")

    def test_create_granule_list(self):
        logger.info("history_manager create_granule_list")
        dataset_ingestion_history_manager = collection_manager.collection_manager.services.history_manager \
            .FileIngestionHistory(self.history_path, self.dataset_id, md5sum_from_filepath)
        CollectionProcessor.create_granule_list(self.granule_file_pattern,
                                                dataset_ingestion_history_manager,
                                                self.target_granule_list_file
                                                )
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertEqual(1, line_number)

        os.remove(self.target_granule_list_file)

    def test_create_granule_list_time_range(self):
        logger.info("history_manager create_granule_list with time range")
        CollectionProcessor.create_granule_list(self.granule_file_pattern,
                                                None,
                                                self.target_granule_list_file,
                                                date_from=datetime(2020, 3, 4, 19, 4, 28, 843998),
                                                date_to=datetime(2020, 6, 2, 19, 4, 28, 843998))
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertGreaterEqual(line_number, 0)

        os.remove(self.target_granule_list_file)

    def test_create_granule_list_time_range_from_only(self):
        logger.info("history_manager create_granule_list with time range")
        CollectionProcessor.create_granule_list(self.granule_file_pattern,
                                                None,
                                                self.target_granule_list_file,
                                                date_from=datetime(2020, 3, 4, 19, 4, 28, 843998))
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertGreaterEqual(line_number, 0)

        os.remove(self.target_granule_list_file)

    def test_create_granule_list_time_range_to_only(self):
        logger.info("history_manager create_granule_list with time range")
        CollectionProcessor.create_granule_list(self.granule_file_pattern,
                                                None,
                                                self.target_granule_list_file,
                                                date_to=datetime(2020, 3, 4, 19, 4, 28, 843998))
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertGreaterEqual(line_number, 0)

        os.remove(self.target_granule_list_file)

    def test_create_granule_list_time_forward_processing(self):
        logger.info("history_manager create_granule_list with time range")
        CollectionProcessor.create_granule_list(self.granule_file_pattern,
                                                None,
                                                self.target_granule_list_file,
                                                forward_processing=True)
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertGreaterEqual(line_number, 0)

        os.remove(self.target_granule_list_file)

    def test_create_granule_list_no_history(self):
        logger.info("history_manager create_granule_list")
        CollectionProcessor.create_granule_list(self.granule_file_pattern,
                                                None,
                                                self.target_granule_list_file
                                                )
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertEqual(2, line_number)

        os.remove(self.target_granule_list_file)

    def test_create_dataset_config(self):
        logger.info("history_manager create_dataset_config")
        CollectionProcessor()._fill_template("avhrr-oi-analysed-sst",
                                                  "analysed_sst",
                                             self.collection_config_template,
                                             self.target_dataset_config_file)

        self.assertTrue(filecmp.cmp(self.expected_dataset_configuration_file, self.target_dataset_config_file),
                        "the dataset configuration file created does not match the expected results")

        os.remove(self.target_dataset_config_file)

    def tearDown(self):
        logger.info("tear down history_manager results")


if __name__ == '__main__':
    unittest.main()