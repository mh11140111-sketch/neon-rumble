plugins {
    id("com.android.application")
}

android {
    namespace = "com.neonrumble.offline"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.neonrumble.offline"
        minSdk = 23
        targetSdk = 35
        versionCode = 347
        versionName = "3.47"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
