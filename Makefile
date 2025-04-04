all: \
	dockers/base/.Dockerfile.3.9.stamp \
	dockers/base/.Dockerfile.3.10.stamp \
	dockers/base/.Dockerfile.3.11.stamp \
	dockers/base/.Dockerfile.3.12.stamp \
	dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/.Dockerfile.stamp \
	dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/.Dockerfile.stamp \
	dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/.Dockerfile.stamp \
	dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/.Dockerfile.stamp \
	dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp \
	$(NULL) \

dockers/base/.Dockerfile.3.9.stamp: dockers/base/Dockerfile.3.9 
	docker build --network=host -t th4tkh13m/vulnbench-base:3.9 -f dockers/base/Dockerfile.3.9 .
	touch dockers/base/.Dockerfile.3.9.stamp
dockers/base/.Dockerfile.3.10.stamp: dockers/base/Dockerfile.3.10
	docker build --network=host -t th4tkh13m/vulnbench-base:3.10 -f dockers/base/Dockerfile.3.10 .
	touch dockers/base/.Dockerfile.3.10.stamp
dockers/base/.Dockerfile.3.11.stamp: dockers/base/Dockerfile.3.11
	docker build --network=host -t th4tkh13m/vulnbench-base:3.11 -f dockers/base/Dockerfile.3.11 .
	touch dockers/base/.Dockerfile.3.11.stamp
dockers/base/.Dockerfile.3.12.stamp: dockers/base/Dockerfile.3.12
	docker build --network=host -t th4tkh13m/vulnbench-base:3.12 -f dockers/base/Dockerfile.3.12 .
	touch dockers/base/.Dockerfile.3.12.stamp
dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/.Dockerfile.stamp: dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/Dockerfile dockers/base/.Dockerfile.3.12.stamp
	docker build --network=host -t th4tkh13m/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816 -f dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/Dockerfile .
	touch dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/.Dockerfile.stamp
dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/.Dockerfile.stamp: dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676 -f dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/Dockerfile .
	touch dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/.Dockerfile.stamp
dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/.Dockerfile.stamp: dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c -f dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/Dockerfile .
	touch dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/.Dockerfile.stamp
dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/.Dockerfile.stamp: dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5 -f dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/Dockerfile .
	touch dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/.Dockerfile.stamp
dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp: dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/Dockerfile dockers/base/.Dockerfile.3.10.stamp
	docker build --network=host -t th4tkh13m/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17 -f dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/Dockerfile .
	touch dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp

clean:
	rm -f \
		dockers/base/.Dockerfile.3.9.stamp \
		dockers/base/.Dockerfile.3.10.stamp \
		dockers/base/.Dockerfile.3.11.stamp \
		dockers/base/.Dockerfile.3.12.stamp \
		dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/.Dockerfile.stamp \
		dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/.Dockerfile.stamp \
		dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/.Dockerfile.stamp \
		dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/.Dockerfile.stamp \
		dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp \
		$(NULL)

.PHONY: all clean
.DEFAULT_GOAL := all