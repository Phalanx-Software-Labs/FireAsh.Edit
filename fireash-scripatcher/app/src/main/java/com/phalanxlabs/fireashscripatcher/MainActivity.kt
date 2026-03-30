package com.phalanxlabs.fireashscripatcher

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.DocumentsContract
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.documentfile.provider.DocumentFile
import com.phalanxlabs.fireashscripatcher.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var treeUri: Uri? = null

    private val prefs by lazy {
        getSharedPreferences("fireash_installer", Context.MODE_PRIVATE)
    }

    private val openTree = registerForActivityResult(
        object : ActivityResultContracts.OpenDocumentTree() {
            override fun createIntent(context: Context, input: Uri?): Intent {
                return super.createIntent(context, input).apply {
                    addFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
                }
            }
        }
    ) { uri ->
        if (uri != null) {
            contentResolver.takePersistableUriPermission(
                uri,
                Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            )
            treeUri = uri
            prefs.edit().putString(KEY_TREE, uri.toString()).apply()
            updateFolderLabel()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        treeUri = prefs.getString(KEY_TREE, null)?.let { Uri.parse(it) }
        updateFolderLabel()
        binding.btnPick.setOnClickListener { openTree.launch(null) }
        binding.btnInstall.setOnClickListener { installPatch() }
    }

    private fun updateFolderLabel() {
        binding.tvFolder.text = treeUri?.toString() ?: "(none selected)"
    }

    private fun toast(msg: String) {
        Toast.makeText(this, msg, Toast.LENGTH_LONG).show()
    }

    private fun installPatch() {
        val tree = treeUri ?: run {
            toast("Choose the game folder first.")
            return
        }
        val root = DocumentFile.fromTreeUri(this, tree) ?: run {
            toast("Could not open that folder.")
            return
        }
        val data = root.findFile("Data") ?: root.findFile("data") ?: run {
            toast("No Data folder here. Pick the folder that contains Data (next to Game.exe).")
            return
        }
        val bytes = try {
            assets.open(ASSET_PATCH).use { it.readBytes() }
        } catch (e: Exception) {
            toast("Missing $ASSET_PATCH in APK assets.")
            return
        }
        if (bytes.isEmpty()) {
            toast("Patched script file in APK is empty.")
            return
        }
        val resolver = contentResolver
        val existing = data.findFile("Scripts.rxdata")
        try {
            if (existing != null && existing.exists()) {
                data.findFile("Scripts.rxdata.backup")?.delete()
                val backup = data.createFile("application/octet-stream", "Scripts.rxdata.backup")
                    ?: run {
                        toast("Could not create Scripts.rxdata.backup")
                        return
                    }
                resolver.openInputStream(existing.uri).use { input ->
                    resolver.openOutputStream(backup.uri).use { output ->
                        input!!.copyTo(output!!)
                    }
                }
            }
            data.findFile(PATCH_TEMP_NAME)?.delete()
            val tmp = data.createFile("application/octet-stream", PATCH_TEMP_NAME)
                ?: run {
                    toast("Could not create temp file in Data.")
                    return
                }
            resolver.openOutputStream(tmp.uri).use { out ->
                out!!.write(bytes)
                out.flush()
            }
            if (existing != null && existing.exists()) {
                val deleted = try {
                    DocumentsContract.deleteDocument(resolver, existing.uri)
                } catch (_: Exception) {
                    false
                }
                if (!deleted) {
                    existing.delete()
                }
            }
            val renamed = try {
                DocumentsContract.renameDocument(resolver, tmp.uri, "Scripts.rxdata")
            } catch (_: Exception) {
                null
            }
            if (renamed == null) {
                val dest = data.createFile("application/octet-stream", "Scripts.rxdata")
                    ?: run {
                        toast("Rename failed and could not create Scripts.rxdata.")
                        return
                    }
                resolver.openInputStream(tmp.uri).use { input ->
                    resolver.openOutputStream(dest.uri).use { output ->
                        input!!.copyTo(output!!)
                    }
                }
                tmp.delete()
            }
            toast("Installed. Open the game in JoiPlay. Backup: Scripts.rxdata.backup")
        } catch (e: Exception) {
            toast("Error: ${e.message}")
        }
    }

    companion object {
        private const val KEY_TREE = "tree_uri"
        private const val ASSET_PATCH = "patched_Scripts.rxdata"
        private const val PATCH_TEMP_NAME = "patchtmp.rxdata"
    }
}
