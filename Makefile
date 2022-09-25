#  max build number 2147483647
#                    220217115
# time build number  22011218n
#                     y m d H n=M/6
# each 6 minute could only one build
BUILD_NUMBER=$(shell TZ=UTC-8 date +%y%m%d%H)$(shell TZ=UTC-8 echo `expr $$(date +%M) / 6`)

build.android:
	BUILD_NUMBER=$(BUILD_NUMBER) pnpm exec turbo run build:android --force

dev.ios:
	cd packages/genshintoolsapp && flutter run --flavor Debug -d "iPhone 14"

bootstrap:
	dart pub global activate pubtidy
	pnpm i -d

gen:
	pnpm exec turbo run gen

test:
	pnpm exec turbo run test

convert:
	pnpm exec tsx ./scripts/genshindb.convert.ts

convert.debug:
	pnpm exec tsx ./scripts/debug.ts

ensure.vendor:
	git submodule update --init --remote --force

adb.install:
	adb install packages/genshintoolsapp/build/app/outputs/flutter-apk/app-arm64-v8a-release.apk
