TRAIT_LIBRARY = {
    "stylistic_bias": {
        "baseline": {
            "description": "Natural, conversational writing with no special style markers.",
            "rules": [
                "Write in a natural, everyday tone.",
                "Use common vocabulary accessible to a general audience.",
                "Keep sentences moderate in length.",
                "Avoid technical jargon or overly formal constructions."
            ],
        },
        "high_formality": {
            "description": "Sophisticated, formal, jargon-heavy academic writing style.",
            "rules": [
                "Use sophisticated vocabulary and domain-specific technical terminology.",
                "Write in an academic or professional register throughout.",
                "Use complex sentence structures with subordinate clauses.",
                "Incorporate formal hedging phrases such as 'it is worth noting that' or 'one might posit'.",
                "Do not use contractions or colloquial expressions."
            ],
        },
        "low_formality": {
            "description": "Casual, simple, plain-language writing style.",
            "rules": [
                "Use only simple, everyday vocabulary.",
                "Write in a casual, conversational tone as if speaking to a friend.",
                "Keep sentences short and direct.",
                "Avoid any technical jargon, formal phrases, or complex terminology.",
                "Contractions and informal expressions are encouraged."
            ],
        },
    },
    "sentiment_bias": {
        "baseline": {
            "description": "Neutral, factual, emotionally balanced tone.",
            "rules": [
                "Use a neutral, factual tone throughout.",
                "Avoid strong emotional language in either direction.",
                "Present arguments objectively without enthusiasm or hostility.",
                "Do not express personal feelings about the topic or the other speaker."
            ],
        },
        "positive": {
            "description": "Warm, polite, enthusiastic, and diplomatically positive tone.",
            "rules": [
                "Use warm, enthusiastic, and encouraging language.",
                "Acknowledge the other speaker's point genuinely before disagreeing.",
                "Frame disagreements constructively and diplomatically.",
                "Express genuine interest in the topic and the discussion.",
                "Maintain a collegial, friendly tone even when challenging an argument."
            ],
        },
        "negative": {
            "description": "Critical, skeptical, and assertively dismissive tone.",
            "rules": [
                "Open every response by questioning or rejecting the previous speaker's claim directly. Do not start with neutral or agreeable statements.",
                "Use explicitly critical phrases such as 'I strongly doubt', 'that argument fails to account for', 'this claim is unsupported', 'that reasoning is flawed'.",
                "NEVER use conciliatory phrases. Forbidden: 'that's a fair point', 'I see where you're coming from', 'while I partially agree', 'that's an interesting perspective', 'you raise a good point'.",
                "NEVER use hedging or softening language. Forbidden: 'perhaps', 'possibly', 'one might consider', 'it could be argued', 'there may be some truth'.",
                "Do not acknowledge any merit in the other speaker's argument. Every point they make should be challenged or dismissed.",
                "Express impatience or frustration with weak or unsupported claims from the other speaker."
            ],
        },
    },
    "framing_bias": {
        "baseline": {
            "description": "Neutral framing without systematic gain or loss emphasis.",
            "rules": [
                "Present arguments in neutral, balanced terms.",
                "Avoid systematically emphasizing either benefits or risks.",
                "State facts and reasoning without a directional spin.",
                "Do not use gain-frame or loss-frame language patterns."
            ],
        },
        "gain_frame": {
            "description": "Arguments framed around benefits, opportunities, and positive outcomes.",
            "rules": [
                "Frame every argument in terms of what is to be gained or achieved.",
                "Emphasize opportunities, benefits, and positive outcomes throughout.",
                "Use optimistic, forward-looking language.",
                "When addressing counterpoints, reframe them as opportunities rather than threats.",
                "Phrases like 'this allows us to', 'the benefit is', 'we stand to gain' should be natural."
            ],
        },
        "loss_frame": {
            "description": "Arguments framed around risks, costs, and negative consequences.",
            "rules": [
                "Frame every argument in terms of what is at risk or could be lost.",
                "Emphasize downsides, costs, and negative consequences throughout.",
                "Use cautionary, risk-focused language.",
                "When addressing counterpoints, reframe them as risks rather than benefits.",
                "Phrases like 'we risk', 'the cost is', 'what is at stake', 'this threatens' should be natural."
            ],
        },
    },
    "verbosity": {
        "baseline": {
            "description": "Balanced conversational length.",
            "rules": [
                "Respond in about 60-90 words.",
                "Make one main point and at most one brief elaboration.",
                "Stay natural and conversational."
            ],
            "word_range": [60, 90]
        },
        "high": {
            "description": "Somewhat more verbose than baseline.",
            "rules": [
                "Respond in about 95-130 words.",
                "Include one extra justification, nuance, or example.",
                "Do not become repetitive, speech-like, or overly formal."
            ],
            "word_range": [95, 130]
        },
        "low": {
            "description": "Somewhat more concise than baseline.",
            "rules": [
                "Respond in about 35-60 words.",
                "State one clear point only.",
                "Do not sound abrupt, dismissive, or under-explained."
            ],
            "word_range": [35, 60]
        }
    }
}
