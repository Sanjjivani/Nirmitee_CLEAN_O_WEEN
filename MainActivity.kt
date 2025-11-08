package com.cleanearth.app

import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.webkit.*
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.*

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var progressBar: ProgressBar
    private val PERMISSION_REQUEST_CODE = 100

    // 🔧 FILE UPLOAD FIX - Add these variables
    private var filePathCallback: ValueCallback<Array<Uri>>? = null
    private val FILE_CHOOSER_RESULT_CODE = 1

    // 🔧 CONFIGURATION: Replace with your website URL
    private val WEBSITE_URL = "http://192.168.1.9:5000"

    // 🔧 AI SIMULATION
    private var isAIModelLoaded = false
    private val garbageTypes = listOf("plastic", "paper", "glass", "metal", "organic")
    private val cleanupPriorities = listOf("low", "medium", "high")

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initializeViews()
        setupWebView()
        checkPermissions()

        // 🔧 Initialize AI Simulation
        initializeAISimulation()
    }

    private fun initializeViews() {
        webView = findViewById(R.id.webView)
        progressBar = findViewById(R.id.progressBar)
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val webSettings = webView.settings

        // Enable JavaScript
        webSettings.javaScriptEnabled = true
        webSettings.domStorageEnabled = true
        webSettings.databaseEnabled = true

        // Enable caching
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT

        // Enable zoom and responsive design
        webSettings.setSupportZoom(true)
        webSettings.builtInZoomControls = true
        webSettings.displayZoomControls = false
        webSettings.useWideViewPort = true
        webSettings.loadWithOverviewMode = true

        // Enable file uploads
        webSettings.allowFileAccess = true
        webSettings.allowContentAccess = true
        webSettings.allowFileAccessFromFileURLs = true
        webSettings.allowUniversalAccessFromFileURLs = true

        // Set WebView client
        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                progressBar.visibility = ProgressBar.VISIBLE
                super.onPageStarted(view, url, favicon)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                progressBar.visibility = ProgressBar.GONE

                // 🔧 Inject JavaScript interface for AI analysis
                injectJavascriptInterface()
                super.onPageFinished(view, url)
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                progressBar.visibility = ProgressBar.GONE
                showErrorPage()
                super.onReceivedError(view, request, error)
            }
        }

        // 🔧 FIXED Chrome client with file upload support
        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progressBar.progress = newProgress
                if (newProgress == 100) {
                    progressBar.visibility = ProgressBar.GONE
                }
            }

            // 🔧 FIX FILE UPLOAD - Add this method
            override fun onShowFileChooser(
                webView: WebView?,
                filePathCallback: ValueCallback<Array<Uri>>?,
                fileChooserParams: FileChooserParams?
            ): Boolean {
                this@MainActivity.filePathCallback?.onReceiveValue(null)
                this@MainActivity.filePathCallback = filePathCallback

                val intent = fileChooserParams?.createIntent()
                try {
                    // 🔧 FIX: Use non-null intent with safe call
                    startActivityForResult(intent ?: createDefaultIntent(), FILE_CHOOSER_RESULT_CODE)
                } catch (e: Exception) {
                    // If no file chooser available, open gallery directly
                    startActivityForResult(createDefaultIntent(), FILE_CHOOSER_RESULT_CODE)
                }
                return true
            }
        }

        // 🔧 Add JavaScript interface for AI communication
        webView.addJavascriptInterface(WebAppInterface(), "AndroidAI")

        // Load the website
        webView.loadUrl(WEBSITE_URL)
    }

    // 🔧 FIX: Create default intent for file chooser
    private fun createDefaultIntent(): Intent {
        val intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.type = "image/*"
        return intent
    }

    // 🔧 ADD THIS METHOD to handle file selection result
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == FILE_CHOOSER_RESULT_CODE) {
            if (filePathCallback == null) return

            val results = when {
                resultCode == RESULT_OK && data != null -> {
                    // Handle the selected file
                    arrayOf(data.data ?: return)
                }
                else -> null
            }

            filePathCallback?.onReceiveValue(results)
            filePathCallback = null
        }
    }

    // 🔧 JAVASCRIPT INTERFACE FOR AI COMMUNICATION
    inner class WebAppInterface {
        @JavascriptInterface
        fun analyzeCleanupImage(imageData: String) {
            // Called from web app when user wants AI analysis
            CoroutineScope(Dispatchers.Main).launch {
                performAIAnalysis(imageData)
            }
        }

        @JavascriptInterface
        fun getAIModelStatus(): String {
            return if (isAIModelLoaded) {
                "READY"
            } else {
                "LOADING"
            }
        }

        @JavascriptInterface
        fun simulateGarbageDetection(): String {
            // For quick testing - simulates AI detection
            return """{
                "has_garbage": true,
                "confidence": 0.92,
                "garbage_types": ["plastic", "paper"],
                "cleanup_priority": "high",
                "analysis_time": "${Date().time}"
            }"""
        }
    }

    // 🔧 AI SIMULATION
    private fun initializeAISimulation() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Simulate AI model loading
                loadAIModelSimulation()

            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this@MainActivity,
                        "AI Simulation initialized",
                        Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun loadAIModelSimulation() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Simulate model download and loading (3 seconds)
                kotlinx.coroutines.delay(3000)

                isAIModelLoaded = true

                runOnUiThread {
                    Toast.makeText(this@MainActivity,
                        "🤖 AI Garbage Detection Ready!",
                        Toast.LENGTH_LONG).show()
                }

            } catch (e: Exception) {
                // Even if simulation fails, mark as ready for demo
                isAIModelLoaded = true
            }
        }
    }

    private fun performAIAnalysis(imageData: String) {
        if (!isAIModelLoaded) {
            sendAnalysisResultToWeb("""{
                "error": "AI model still loading",
                "has_garbage": false,
                "confidence": 0.0
            }""")
            return
        }

        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Simulate AI processing time
                kotlinx.coroutines.delay(2000)

                // 🔧 SIMULATED AI ANALYSIS
                val analysisResult = simulateAIAnalysis(imageData)

                runOnUiThread {
                    sendAnalysisResultToWeb(analysisResult)
                }

            } catch (e: Exception) {
                runOnUiThread {
                    sendAnalysisResultToWeb("""{
                        "error": "Analysis failed: ${e.message}",
                        "has_garbage": false,
                        "confidence": 0.0
                    }""")
                }
            }
        }
    }

    private fun simulateAIAnalysis(imageData: String): String {
        // 🔧 REALISTIC AI SIMULATION FOR DEMO
        val random = Random()
        val hasGarbage = random.nextBoolean() || random.nextDouble() > 0.3 // 70% chance of garbage

        if (hasGarbage) {
            val confidence = 0.7 + random.nextDouble() * 0.3 // 70-100% confidence
            val detectedTypes = garbageTypes.shuffled().take(random.nextInt(3) + 1)
            val priority = cleanupPriorities.random()

            return """{
                "has_garbage": true,
                "confidence": $confidence,
                "garbage_types": ${detectedTypes},
                "cleanup_priority": "$priority",
                "analysis_time": "${Date().time}",
                "message": "AI detected ${detectedTypes.joinToString(", ")}"
            }"""
        } else {
            return """{
                "has_garbage": false,
                "confidence": ${0.3 + random.nextDouble() * 0.4},
                "garbage_types": [],
                "cleanup_priority": "none",
                "analysis_time": "${Date().time}",
                "message": "No garbage detected - area looks clean!"
            }"""
        }
    }

    private fun sendAnalysisResultToWeb(resultJson: String) {
        val jsCode = "if (window.handleAIAnalysisResult) { window.handleAIAnalysisResult($resultJson); }"
        webView.evaluateJavascript(jsCode, null)

        // Also show Toast notification
        runOnUiThread {
            Toast.makeText(this, "🤖 AI Analysis Complete!", Toast.LENGTH_SHORT).show()
        }
    }

    private fun injectJavascriptInterface() {
        val jsCode = """
            // Create global function for AI analysis
            window.analyzeWithAI = function(imageData) {
                AndroidAI.analyzeCleanupImage(imageData);
            };
            
            // Check AI status
            window.getAIStatus = function() {
                return AndroidAI.getAIModelStatus();
            };
            
            // Quick test function
            window.testAI = function() {
                return AndroidAI.simulateGarbageDetection();
            };
            
            console.log('🤖 AI Interface injected successfully');
            
            // Auto-show AI status
            setTimeout(function() {
                const status = window.getAIStatus();
                if (status === 'READY') {
                    console.log('🚀 AI Garbage Detection is READY!');
                    // Show AI ready notification
                    if (window.showNotification) {
                        window.showNotification('🤖 AI Garbage Detection Ready!', 'success');
                    }
                }
            }, 1000);
        """.trimIndent()

        webView.evaluateJavascript(jsCode, null)
    }

    private fun checkPermissions() {
        val permissions = arrayOf(
            android.Manifest.permission.INTERNET,
            android.Manifest.permission.ACCESS_NETWORK_STATE,
            android.Manifest.permission.READ_EXTERNAL_STORAGE,
            android.Manifest.permission.WRITE_EXTERNAL_STORAGE
        )

        val permissionsToRequest = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }

        if (permissionsToRequest.isNotEmpty()) {
            ActivityCompat.requestPermissions(
                this,
                permissionsToRequest.toTypedArray(),
                PERMISSION_REQUEST_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.all { it == PackageManager.PERMISSION_GRANTED }) {
                // Permissions granted, reload webview
                webView.reload()
            }
        }
    }

    private fun showErrorPage() {
        val errorHtml = """
            <html>
                <body style='text-align:center; padding:50px; font-family:Arial;'>
                    <h2>⚠️ Connection Error</h2>
                    <p>Unable to load CleanEarth website.</p>
                    <button onclick='retry()' 
                            style='padding:10px 20px; background:#2E8B57; color:white; border:none; border-radius:5px;'>
                        Retry
                    </button>
                </body>
                <script>
                    function retry() {
                        window.location.reload();
                    }
                </script>
            </html>
        """.trimIndent()

        webView.loadDataWithBaseURL(null, errorHtml, "text/html", "UTF-8", null)
    }

    // Handle back button in WebView
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}