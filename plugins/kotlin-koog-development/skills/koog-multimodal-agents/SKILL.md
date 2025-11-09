---
name: koog-multimodal-agents
description: Building multimodal AI agents with vision, document processing, audio, and structured output capabilities. Covers image analysis, PDF processing, vision-language models, structured data extraction, and content moderation. Use when building agents that process images, documents, audio, or require structured JSON output with validation.
---

# Koog Multimodal Agents

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Building agents that analyze images and photos
- Processing PDF documents and extracting information
- Creating vision-language agents for multimodal tasks
- Implementing structured output with JSON schemas
- Building document understanding systems
- Creating OCR and text extraction agents
- Implementing content moderation for images and text
- Building agents that generate validated structured data
- Processing mixed media inputs (text + images + documents)
- Creating agents with audio processing capabilities

## Core Concepts

### Vision-Enabled Agents

#### Basic Image Analysis

```kotlin
import ai.koog.agent
import ai.koog.prompt.*

val imageAnalyzer = agent("image_analyzer") {
    instruction("""
        Analyze images and provide detailed descriptions.
        Include: objects, people, setting, colors, mood, and any text visible.
    """)

    // Enable vision capability
    capabilities {
        vision = true
    }

    llmProvider = OpenAiLLMClient(
        modelId = "gpt-4-vision-preview",
        apiKey = config.openAiKey
    )
}

// Execute with image
suspend fun analyzeImage(imageUrl: String): String {
    val prompt = Prompt {
        userMessage {
            text("Describe this image in detail")
            attachment(ImageAttachment(url = imageUrl))
        }
    }

    return imageAnalyzer.execute(prompt)
}
```

#### Multi-Image Comparison

```kotlin
val imageComparator = agent("image_comparator") {
    instruction("""
        Compare multiple images and identify:
        - Similarities and differences
        - Common objects or themes
        - Chronological order if applicable
        - Any anomalies or unique elements
    """)

    capabilities {
        vision = true
    }
}

suspend fun compareImages(imageUrls: List<String>): String {
    val prompt = Prompt {
        userMessage {
            text("Compare these images and describe their similarities and differences")

            imageUrls.forEach { url ->
                attachment(ImageAttachment(url = url))
            }
        }
    }

    return imageComparator.execute(prompt)
}
```

#### Vision-Based Tool Integration

```kotlin
class ImageAnalysisTool : Tool {
    override val name = "analyze_image"
    override val description = "Analyze image and extract information"

    private val visionModel = OpenAiLLMClient(
        modelId = "gpt-4-vision-preview"
    )

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val imageUrl = arguments["image_url"] as? String
            ?: return ToolResult.error("Missing image_url")

        val analysisType = arguments["analysis_type"] as? String ?: "general"

        val prompt = when (analysisType) {
            "ocr" -> "Extract all text from this image"
            "objects" -> "List all objects visible in this image"
            "people" -> "Describe the people in this image"
            "scene" -> "Describe the scene and setting"
            else -> "Provide a detailed analysis of this image"
        }

        val result = visionModel.execute(
            Prompt {
                userMessage {
                    text(prompt)
                    attachment(ImageAttachment(url = imageUrl))
                }
            }
        )

        return ToolResult.success(mapOf(
            "analysis" to result,
            "image_url" to imageUrl,
            "analysis_type" to analysisType
        ))
    }
}

// Use in agent
val agent = agent("vision_agent") {
    instruction("Analyze images using the vision tool")

    tool("analyze_image", ImageAnalysisTool())
}
```

### Document Processing

#### PDF Document Analysis

```kotlin
import ai.koog.prompt.*

val pdfAnalyzer = agent("pdf_analyzer") {
    instruction("""
        Extract and analyze information from PDF documents.
        Provide structured summaries including:
        - Document type and purpose
        - Key information and data
        - Tables and figures
        - Action items or conclusions
    """)

    capabilities {
        vision = true // Required for PDF image rendering
        documents = true
    }
}

suspend fun analyzePdf(pdfPath: String): DocumentAnalysis {
    val prompt = Prompt {
        userMessage {
            text("Analyze this document and extract key information")
            attachment(DocumentAttachment(
                path = pdfPath,
                mimeType = "application/pdf"
            ))
        }
    }

    val result = pdfAnalyzer.executeStructured<DocumentAnalysis>(prompt)
    return result
}

@Serializable
data class DocumentAnalysis(
    @LLMDescription("Type of document (invoice, contract, report, etc.)")
    val documentType: String,

    @LLMDescription("Main subject or title")
    val title: String,

    @LLMDescription("Key information extracted")
    val keyInformation: List<String>,

    @LLMDescription("Dates mentioned in the document")
    val dates: List<String>,

    @LLMDescription("Financial amounts if any")
    val amounts: List<String>?,

    @LLMDescription("Action items or next steps")
    val actionItems: List<String>?
)
```

#### Multi-Page Document Processing

```kotlin
class DocumentProcessor {

    suspend fun processMultiPageDocument(
        pdfPath: String,
        pageRange: IntRange? = null
    ): List<PageAnalysis> {
        val pdf = PDDocument.load(File(pdfPath))
        val pages = pageRange?.let { range ->
            pdf.pages.toList().slice(range)
        } ?: pdf.pages.toList()

        return pages.mapIndexed { index, page ->
            analyzePage(page, index + 1)
        }.also {
            pdf.close()
        }
    }

    private suspend fun analyzePage(page: PDPage, pageNumber: Int): PageAnalysis {
        // Convert page to image
        val imageBytes = renderPageToImage(page)

        val prompt = Prompt {
            userMessage {
                text("Analyze page $pageNumber")
                attachment(ImageAttachment(
                    data = imageBytes,
                    mimeType = "image/png"
                ))
            }
        }

        val analysis = agent.execute(prompt)

        return PageAnalysis(
            pageNumber = pageNumber,
            content = analysis,
            hasImages = detectImages(page),
            hasTable = detectTables(page)
        )
    }
}

data class PageAnalysis(
    val pageNumber: Int,
    val content: String,
    val hasImages: Boolean,
    val hasTable: Boolean
)
```

#### Table Extraction from Documents

```kotlin
val tableExtractor = agent("table_extractor") {
    instruction("""
        Extract tables from documents and convert to structured data.
        Return tables as JSON arrays with headers and rows.
    """)

    capabilities {
        vision = true
        documents = true
    }
}

@Serializable
data class ExtractedTable(
    @LLMDescription("Table title or caption")
    val title: String?,

    @LLMDescription("Column headers")
    val headers: List<String>,

    @LLMDescription("Table rows, each row is a list of cell values")
    val rows: List<List<String>>,

    @LLMDescription("Page number where table was found")
    val pageNumber: Int
)

suspend fun extractTables(pdfPath: String): List<ExtractedTable> {
    val prompt = Prompt {
        userMessage {
            text("Extract all tables from this document")
            attachment(DocumentAttachment(path = pdfPath))
        }
    }

    return tableExtractor.executeStructured<List<ExtractedTable>>(prompt)
}
```

### Structured Output with Validation

#### Type-Safe Data Extraction

```kotlin
import kotlinx.serialization.*
import ai.koog.structured.*

@Serializable
data class UserProfile(
    @LLMDescription("User's full name")
    val fullName: String,

    @LLMDescription("Email address")
    val email: String,

    @LLMDescription("Age (must be 18 or older)")
    val age: Int,

    @LLMDescription("Phone number in international format")
    val phone: String,

    @LLMDescription("List of interests or hobbies")
    val interests: List<String>,

    @LLMDescription("Employment status: employed, unemployed, student, retired")
    val employmentStatus: String,

    @LLMDescription("City of residence")
    val city: String
)

val profileExtractor = agent("profile_extractor") {
    instruction("""
        Extract user profile information from text.
        Ensure all fields are accurately extracted and validated.
    """)
}

suspend fun extractProfile(text: String): UserProfile {
    val session = profileExtractor.createWriteSession()

    val profile = session.requestLLMStructured<UserProfile>(
        prompt = text,
        retryCount = 3, // Auto-retry if validation fails
        validator = { profile ->
            // Custom validation
            require(profile.age >= 18) { "Age must be 18 or older" }
            require(profile.email.contains("@")) { "Invalid email format" }
            require(profile.employmentStatus in listOf(
                "employed", "unemployed", "student", "retired"
            )) { "Invalid employment status" }
        }
    )

    return profile
}
```

#### Complex Nested Structures

```kotlin
@Serializable
data class InvoiceData(
    @LLMDescription("Invoice number")
    val invoiceNumber: String,

    @LLMDescription("Invoice date in ISO format")
    val date: String,

    @LLMDescription("Due date in ISO format")
    val dueDate: String,

    @LLMDescription("Vendor information")
    val vendor: CompanyInfo,

    @LLMDescription("Customer information")
    val customer: CompanyInfo,

    @LLMDescription("Line items")
    val lineItems: List<LineItem>,

    @LLMDescription("Subtotal amount")
    val subtotal: Double,

    @LLMDescription("Tax amount")
    val tax: Double,

    @LLMDescription("Total amount")
    val total: Double,

    @LLMDescription("Payment terms")
    val paymentTerms: String?
)

@Serializable
data class CompanyInfo(
    @LLMDescription("Company name")
    val name: String,

    @LLMDescription("Street address")
    val address: String,

    @LLMDescription("City")
    val city: String,

    @LLMDescription("Postal code")
    val postalCode: String,

    @LLMDescription("Country")
    val country: String,

    @LLMDescription("Tax ID or VAT number")
    val taxId: String?
)

@Serializable
data class LineItem(
    @LLMDescription("Item description")
    val description: String,

    @LLMDescription("Quantity")
    val quantity: Double,

    @LLMDescription("Unit price")
    val unitPrice: Double,

    @LLMDescription("Total price for this line")
    val total: Double
)

val invoiceExtractor = agent("invoice_extractor") {
    instruction("""
        Extract invoice data from documents.
        Parse all fields accurately, including nested company information and line items.
    """)

    capabilities {
        vision = true
        documents = true
    }
}

suspend fun extractInvoice(documentPath: String): InvoiceData {
    val prompt = Prompt {
        userMessage {
            text("Extract complete invoice data")
            attachment(DocumentAttachment(path = documentPath))
        }
    }

    return invoiceExtractor.executeStructured<InvoiceData>(
        prompt,
        retryCount = 3,
        validator = { invoice ->
            // Validate calculations
            val calculatedSubtotal = invoice.lineItems.sumOf { it.total }
            require((calculatedSubtotal - invoice.subtotal).absoluteValue < 0.01) {
                "Subtotal mismatch: calculated $calculatedSubtotal, found ${invoice.subtotal}"
            }

            val calculatedTotal = invoice.subtotal + invoice.tax
            require((calculatedTotal - invoice.total).absoluteValue < 0.01) {
                "Total mismatch: calculated $calculatedTotal, found ${invoice.total}"
            }
        }
    )
}
```

#### JSON Schema Generation

```kotlin
import kotlinx.serialization.json.*

class SchemaGenerator {

    inline fun <reified T> generateSchema(): JsonObject {
        // Generate JSON schema from Kotlin data class
        return buildJsonObject {
            put("type", "object")
            put("properties", generateProperties<T>())
            put("required", generateRequired<T>())
        }
    }

    inline fun <reified T> generateProperties(): JsonObject {
        // Use reflection to generate schema
        return buildJsonObject {
            T::class.members
                .filterIsInstance<KProperty<*>>()
                .forEach { property ->
                    val description = property.findAnnotation<LLMDescription>()?.value
                    put(property.name, buildJsonObject {
                        put("type", inferType(property.returnType))
                        description?.let { put("description", it) }
                    })
                }
        }
    }
}

// Usage
val agent = agent("structured_agent") {
    val schema = SchemaGenerator().generateSchema<UserProfile>()

    instruction("""
        Extract data according to the provided schema.
        Schema: $schema
    """)
}
```

### Content Moderation

#### Text and Image Moderation

```kotlin
import ai.koog.moderation.*

class ModeratedAgent(
    private val agent: Agent,
    private val textModerator: ContentModerator,
    private val imageModerator: ContentModerator
) {

    suspend fun execute(input: String, images: List<String> = emptyList()): String {
        // Moderate text input
        val textModeration = textModerator.moderate(input)
        if (textModeration.isHarmful) {
            throw SecurityException(
                "Input contains harmful content: ${textModeration.categories}"
            )
        }

        // Moderate images
        images.forEach { imageUrl ->
            val imageModeration = imageModerator.moderateImage(imageUrl)
            if (imageModeration.isHarmful) {
                throw SecurityException(
                    "Image contains harmful content: ${imageModeration.categories}"
                )
            }
        }

        // Execute agent
        val output = agent.execute(input)

        // Moderate output
        val outputModeration = textModerator.moderate(output)
        if (outputModeration.isHarmful) {
            logger.warn("Agent output flagged: ${outputModeration.categories}")
            return "I apologize, but I cannot provide that information."
        }

        return output
    }
}

// Setup moderators
val textModerator = OpenAiModerator(apiKey = config.openAiKey)
val imageModerator = OpenAiImageModerator(apiKey = config.openAiKey)

val safeAgent = ModeratedAgent(
    agent = myAgent,
    textModerator = textModerator,
    imageModerator = imageModerator
)
```

#### Custom Moderation Rules

```kotlin
class CustomModerationEngine {

    private val bannedWords = loadBannedWords()
    private val suspiciousPatterns = loadPatterns()

    fun moderate(content: String): ModerationResult {
        val violations = mutableListOf<String>()

        // Check for banned words
        bannedWords.forEach { word ->
            if (content.contains(word, ignoreCase = true)) {
                violations.add("banned_word:$word")
            }
        }

        // Check for suspicious patterns
        suspiciousPatterns.forEach { (name, pattern) ->
            if (pattern.containsMatchIn(content)) {
                violations.add("pattern:$name")
            }
        }

        // Check for PII
        if (containsPII(content)) {
            violations.add("contains_pii")
        }

        return ModerationResult(
            isHarmful = violations.isNotEmpty(),
            categories = violations,
            confidence = calculateConfidence(violations)
        )
    }

    private fun containsPII(content: String): Boolean {
        val emailPattern = Regex("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
        val phonePattern = Regex("\\+?\\d{1,3}[-.]?\\d{3,4}[-.]?\\d{4}")
        val ssnPattern = Regex("\\d{3}-\\d{2}-\\d{4}")

        return emailPattern.containsMatchIn(content) ||
               phonePattern.containsMatchIn(content) ||
               ssnPattern.containsMatchIn(content)
    }
}

data class ModerationResult(
    val isHarmful: Boolean,
    val categories: List<String>,
    val confidence: Double
)
```

### Advanced Multimodal Patterns

#### Screenshot Analysis Agent

```kotlin
val screenshotAnalyzer = agent("screenshot_analyzer") {
    instruction("""
        Analyze screenshots and provide insights about:
        - UI/UX issues
        - Errors or bugs visible
        - Accessibility concerns
        - Design improvements
    """)

    capabilities {
        vision = true
    }
}

@Serializable
data class ScreenshotAnalysis(
    @LLMDescription("Type of interface: web, mobile, desktop")
    val interfaceType: String,

    @LLMDescription("Identified UI issues")
    val uiIssues: List<String>,

    @LLMDescription("Visible errors or bugs")
    val errors: List<String>,

    @LLMDescription("Accessibility concerns")
    val accessibilityConcerns: List<String>,

    @LLMDescription("Suggested improvements")
    val improvements: List<String>
)

suspend fun analyzeScreenshot(screenshotPath: String): ScreenshotAnalysis {
    val prompt = Prompt {
        userMessage {
            text("Analyze this screenshot for UI/UX issues and improvements")
            attachment(ImageAttachment(path = screenshotPath))
        }
    }

    return screenshotAnalyzer.executeStructured<ScreenshotAnalysis>(prompt)
}
```

#### Mixed Media Agent

```kotlin
val mixedMediaAgent = agent("mixed_media_processor") {
    instruction("""
        Process and analyze mixed media inputs including text, images, and documents.
        Provide comprehensive analysis that integrates all input types.
    """)

    capabilities {
        vision = true
        documents = true
    }
}

data class MixedMediaInput(
    val text: String,
    val images: List<String>,
    val documents: List<String>
)

suspend fun processMixedMedia(input: MixedMediaInput): String {
    val prompt = Prompt {
        systemMessage("Analyze all provided media and create a comprehensive report")

        userMessage {
            text(input.text)

            input.images.forEach { imageUrl ->
                attachment(ImageAttachment(url = imageUrl))
            }

            input.documents.forEach { docPath ->
                attachment(DocumentAttachment(path = docPath))
            }
        }
    }

    return mixedMediaAgent.execute(prompt)
}
```

#### Diagram and Chart Extraction

```kotlin
val chartExtractor = agent("chart_extractor") {
    instruction("""
        Extract data from charts, graphs, and diagrams.
        Identify chart type and extract all data points accurately.
    """)

    capabilities {
        vision = true
    }
}

@Serializable
data class ChartData(
    @LLMDescription("Type of chart: bar, line, pie, scatter, etc.")
    val chartType: String,

    @LLMDescription("Chart title")
    val title: String,

    @LLMDescription("X-axis label")
    val xAxisLabel: String?,

    @LLMDescription("Y-axis label")
    val yAxisLabel: String?,

    @LLMDescription("Data series")
    val series: List<DataSeries>,

    @LLMDescription("Legend entries")
    val legend: List<String>?
)

@Serializable
data class DataSeries(
    @LLMDescription("Series name")
    val name: String,

    @LLMDescription("Data points")
    val dataPoints: List<DataPoint>
)

@Serializable
data class DataPoint(
    @LLMDescription("X value or category")
    val x: String,

    @LLMDescription("Y value")
    val y: Double
)

suspend fun extractChartData(chartImageUrl: String): ChartData {
    val prompt = Prompt {
        userMessage {
            text("Extract all data from this chart")
            attachment(ImageAttachment(url = chartImageUrl))
        }
    }

    return chartExtractor.executeStructured<ChartData>(prompt)
}
```

### OCR and Text Extraction

```kotlin
val ocrAgent = agent("ocr_extractor") {
    instruction("""
        Extract all text from images using OCR.
        Preserve formatting, layout, and structure when possible.
    """)

    capabilities {
        vision = true
    }
}

@Serializable
data class OCRResult(
    @LLMDescription("Extracted text")
    val text: String,

    @LLMDescription("Detected language")
    val language: String,

    @LLMDescription("Confidence score 0-1")
    val confidence: Double,

    @LLMDescription("Text regions found")
    val regions: List<TextRegion>
)

@Serializable
data class TextRegion(
    @LLMDescription("Text content")
    val text: String,

    @LLMDescription("Approximate position: top, middle, bottom")
    val position: String,

    @LLMDescription("Text size: small, medium, large")
    val size: String
)

suspend fun extractText(imageUrl: String): OCRResult {
    val prompt = Prompt {
        userMessage {
            text("Extract all text from this image with position and size information")
            attachment(ImageAttachment(url = imageUrl))
        }
    }

    return ocrAgent.executeStructured<OCRResult>(prompt)
}
```

## Patterns and Best Practices

### Pattern 1: Progressive Document Processing

```kotlin
suspend fun processDocumentProgressive(pdfPath: String): DocumentReport {
    // Step 1: Get overview
    val overview = getDocumentOverview(pdfPath)

    // Step 2: Extract key sections based on overview
    val sections = extractRelevantSections(pdfPath, overview)

    // Step 3: Deep analysis of critical sections
    val analysis = analyzeSection(sections)

    return DocumentReport(overview, sections, analysis)
}
```

### Pattern 2: Image Preprocessing

```kotlin
class ImagePreprocessor {
    fun prepareForVision(imagePath: String): ProcessedImage {
        val image = ImageIO.read(File(imagePath))

        // Resize if too large
        val resized = if (image.width > 2000 || image.height > 2000) {
            resizeImage(image, 2000)
        } else {
            image
        }

        // Enhance quality
        val enhanced = enhanceImage(resized)

        // Convert to optimal format
        val bytes = imageToBytes(enhanced, "PNG")

        return ProcessedImage(bytes, "image/png")
    }
}
```

### Pattern 3: Validation Pyramid

```kotlin
suspend fun <T> extractWithValidation(
    prompt: Prompt,
    validator: (T) -> Unit
): T {
    var attempts = 0
    val maxAttempts = 3

    while (attempts < maxAttempts) {
        try {
            val result = agent.executeStructured<T>(prompt)
            validator(result)
            return result
        } catch (e: ValidationException) {
            attempts++
            if (attempts >= maxAttempts) throw e

            // Add validation error to prompt for retry
            prompt.append(SystemMessage(
                "Previous extraction failed validation: ${e.message}. " +
                "Please extract again ensuring accuracy."
            ))
        }
    }

    throw ValidationException("Failed after $maxAttempts attempts")
}
```

## Common Pitfalls

### Pitfall 1: Large Image Files

```kotlin
// ✗ Bad: Sending huge images
val result = agent.execute(ImageAttachment(
    url = "https://example.com/10MB-image.jpg"
))

// ✓ Good: Resize before sending
val resized = resizeImage(imageUrl, maxSize = 2000)
val result = agent.execute(ImageAttachment(data = resized))
```

### Pitfall 2: Missing Validation

```kotlin
// ✗ Bad: No validation
val data = agent.executeStructured<InvoiceData>(prompt)
saveToDatabase(data) // May have invalid data!

// ✓ Good: Validate before use
val data = agent.executeStructured<InvoiceData>(
    prompt,
    validator = { invoice ->
        require(invoice.total >= 0) { "Invalid total" }
        require(invoice.lineItems.isNotEmpty()) { "No line items" }
    }
)
saveToDatabase(data)
```

### Pitfall 3: Ignoring Moderation

```kotlin
// ✗ Bad: No content moderation
val result = agent.execute(userInput)

// ✓ Good: Always moderate
val moderation = moderator.moderate(userInput)
if (!moderation.isHarmful) {
    val result = agent.execute(userInput)
}
```

## References

- Related skill: [kotlin-koog-agent-development](/home/user/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md)
- Related skill: [koog-tool-integration](/home/user/agents/plugins/kotlin-koog-development/skills/koog-tool-integration/SKILL.md)
- [Koog Vision Support](https://docs.koog.ai/vision/)
- [Koog Structured Output](https://docs.koog.ai/structured-output/)
- [Koog Content Moderation](https://docs.koog.ai/content-moderation/)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Anthropic Claude Vision](https://docs.anthropic.com/claude/docs/vision)
