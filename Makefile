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
	dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/.Dockerfile.stamp \
	dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/.Dockerfile.stamp \
	dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/.Dockerfile.stamp \
	dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/.Dockerfile.stamp \
	dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/.Dockerfile.stamp \
	dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/.Dockerfile.stamp \
	dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/.Dockerfile.stamp \
	dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/.Dockerfile.stamp \
	dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/.Dockerfile.stamp \
	dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/.Dockerfile.stamp \
	dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/.Dockerfile.stamp \
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
	docker build --network=host -t th4tkh13m/pycqa__bandit__b983c276759233e68ef236ed6f34e07e038327f5 -f dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/Dockerfile .
	touch dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/.Dockerfile.stamp
dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp: dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/Dockerfile dockers/base/.Dockerfile.3.10.stamp
	docker build --network=host -t th4tkh13m/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17 -f dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/Dockerfile .
	touch dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp
dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/.Dockerfile.stamp: dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead -f dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/Dockerfile .
	touch dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/.Dockerfile.stamp
dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/.Dockerfile.stamp: dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27 -f dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/Dockerfile .
	touch dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/.Dockerfile.stamp
dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/.Dockerfile.stamp: dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/Dockerfile dockers/base/.Dockerfile.3.11.stamp
	docker build --network=host -t th4tkh13m/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852 -f dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/Dockerfile .
	touch dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/.Dockerfile.stamp
dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/.Dockerfile.stamp: dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/flexget__flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978 -f dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/Dockerfile .
	touch dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/.Dockerfile.stamp
dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/.Dockerfile.stamp: dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/Dockerfile dockers/base/.Dockerfile.3.11.stamp
	docker build --network=host -t th4tkh13m/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c -f dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/Dockerfile .
	touch dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/.Dockerfile.stamp
dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/.Dockerfile.stamp: dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f -f dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/Dockerfile .
	touch dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/.Dockerfile.stamp
dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/.Dockerfile.stamp: dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/Dockerfile dockers/base/.Dockerfile.3.12.stamp
	docker build --network=host -t th4tkh13m/microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9 -f dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/Dockerfile .
	touch dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/.Dockerfile.stamp
dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/.Dockerfile.stamp: dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/Dockerfile dockers/base/.Dockerfile.3.11.stamp
	docker build --network=host -t th4tkh13m/berriai__litellm__cf86ce390879b6242049a5a53cac52b339a51df3 -f dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/Dockerfile .
	touch dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/.Dockerfile.stamp
dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/.Dockerfile.stamp: dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/Dockerfile dockers/base/.Dockerfile.3.9.stamp
	docker build --network=host -t th4tkh13m/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732 -f dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/Dockerfile .
	touch dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/.Dockerfile.stamp
dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/.Dockerfile.stamp: dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/Dockerfile dockers/base/.Dockerfile.3.12.stamp
	docker build --network=host -t th4tkh13m/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf -f dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/Dockerfile .
	touch dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/.Dockerfile.stamp
dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/.Dockerfile.stamp: dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/Dockerfile dockers/base/.Dockerfile.3.12.stamp
	docker build --network=host -t th4tkh13m/nvidia__nvflare__66f274e24d9d177644bbd6e8ba39be137a15bc6d -f dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/Dockerfile .
	touch dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/.Dockerfile.stamp
	$(NULL)
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
		dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/.Dockerfile.stamp \
		dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/.Dockerfile.stamp \
		dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/.Dockerfile.stamp \
		dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/.Dockerfile.stamp \
		dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/.Dockerfile.stamp \
		dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/.Dockerfile.stamp \
		dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/.Dockerfile.stamp \
		dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/.Dockerfile.stamp \
		dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/.Dockerfile.stamp \
		dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/.Dockerfile.stamp \
		dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/.Dockerfile.stamp \
		$(NULL)

clean-projects:
	rm -f \
		dockers/django__django__efe3ca09e029c63e25f6e19843cb0c68cc7fa816/.Dockerfile.stamp \
		dockers/red-hat-storage__ocs-ci__29c57497850150833cbd5f514b3c40289b6f4676/.Dockerfile.stamp \
		dockers/ytdl-org__youtube-dl__420d53387cff54ea1fccca061438d59bdb50a39c/.Dockerfile.stamp \
		dockers/PyCQA__bandit__b983c276759233e68ef236ed6f34e07e038327f5/.Dockerfile.stamp \
		dockers/transferwise__pipelinewise__3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17/.Dockerfile.stamp \
		dockers/pypa__pipenv__a5a60692461810ec68c9d757918b1442e110eead/.Dockerfile.stamp \
		dockers/faircloth-lab__phyluce__6aa55335d69e742a3e9ba1c6e56d7d776366cb27/.Dockerfile.stamp \
		dockers/obsidianforensics__unfurl__c1f6eda9e9a46a1239b48f667e3ac73176a8c852/.Dockerfile.stamp \
		dockers/Flexget__Flexget__a8697f2bbdfdd045ab0069f770fbd2d709990978/.Dockerfile.stamp \
		dockers/linkml__linkml__3ae9ee399590a03b6840a610e02ff4c944b23b1c/.Dockerfile.stamp \
		dockers/simpeg__simpeg__985593fd655dd4a58443e7be9a938dab6b978a6f/.Dockerfile.stamp \
		dockers/Microsoft__botbuilder-python__bd5662abb1297ebd457ace2918c26e5d611271e9/.Dockerfile.stamp \
		dockers/BerriAI__litellm__cf86ce390879b6242049a5a53cac52b339a51df3/.Dockerfile.stamp \
		dockers/fls-bioinformatics-core__genomics__c181f1c8623355e1ccff120a14c3c61e4059a732/.Dockerfile.stamp \
		dockers/redhatinsights__insights-core__57df3dad1a48cad3c4cfd35487cf64c135aca9bf/.Dockerfile.stamp \
		dockers/NVIDIA__NVFlare__66f274e24d9d177644bbd6e8ba39be137a15bc6d/.Dockerfile.stamp \
		$(NULL)
.PHONY: all clean clean-projects
.DEFAULT_GOAL := all