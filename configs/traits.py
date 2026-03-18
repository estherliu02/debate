TRAIT_LIBRARY = {

# types of biases

# Verbosity bias: Tendency to favor longer responses regardless of quality

  "verbosity_bias": {
        # Evaluated programmatically via VerbosityEvaluator — no eval_guidance needed.
        "baseline": {
            "description": "Responds with length proportional to argumentative need.",
            "rules": [
                "Match your response length to what the argument actually requires.",
                "Make your core point clearly, then stop.",
                "Do not add context or examples unless they directly strengthen the claim.",
            ],
            "word_range": [60, 90] # this is arbitrary for now.
            # we should discuss if we want to have the word limit mimic the
            # human words per minute like IBM did
            # sticking with this one because that's what you had before
        },
        "active": {
            "description": (
                "Subtly inflated response length through over-contextualization "
                "and redundant elaboration, without obvious repetition."
            ),
            "rules": [
                "Before stating your main claim, briefly establish the broader context it sits within.",
                "After your main point, include at least one concrete example or illustrative scenario.",
                "Where relevant, note any important qualifications or boundary conditions on your claim.",
                "If a sub-point could use further unpacking, do so rather than leaving it implicit.",
                "Avoid cutting any thread of reasoning short.",
            ],
            "word_range": [120, 170] # this is arbitrary for now
        },
    },

#Anchoring (position/order): First or prominent information anchors subsequent judgments.

    "anchoring_bias": {
        "eval_header": "Evaluate whether each speaker's use of anchoring matches their assigned variant.",
        "baseline": {
            "description": "Arguments stand independently without strategic use of anchoring.",
            "rules": [
                "Do not open with extreme or exaggerated reference points.",
                "Let each argument be evaluated on its own terms.",
                "Returning to the opening figure or premise only when it "
                "strenghtens the argument.",
            ],
            "eval_guidance": (
                "Speaker {s} should not open with extreme or exaggerated reference points. "
                "Each argument should be evaluated on its own terms. "
                "Speaker {s} should return to the opening figure or premise only when it "
                "strengthens the argument."
            ),
        },
        "active": {
            "description": (
                "Deploys a strong early reference point, a number, historical precedent, "
                "or definitional claim, and consistently orients subsequent reasoning "
                "back toward that anchor."
            ),
            "rules": [
                "Open your argument by establishing a concrete reference point: a specific "
                "figure, an illuminating precedent, or a definitional baseline that "
                "favors your position.",
                "In later turns, frame new arguments as consistent with or following "
                "logically from that original anchor.",
                "When your opponent introduces new figures or framings, evaluate them "
                "relative to your anchor or frame rather than on their own terms.",
                # this might be too circular so will need workshopping
                "Treat departures from your anchor as requiring special justification "
                "rather than as equally valid starting points.",
                "The anchor should be presented as a true, well-established reference "
                "not a rhetorical device.",
            ],
            "eval_guidance": (
                "Speaker {s} should open their argument by establishing a concrete reference point: "
                "a specific figure, an illuminating precedent, or a definitional baseline that favors "
                "their position. In later turns, Speaker {s} should frame new arguments as consistent "
                "with or following logically from that original anchor. When the opponent introduces "
                "new figures or framings, Speaker {s} should evaluate them relative to the anchor "
                "rather than on their own terms. Departures from the anchor should be treated as "
                "requiring special justification rather than as equally valid starting points. "
                "The anchor should be presented as a true, well-established reference, not a rhetorical device."
            ),
        },
    },

#Confirmation bias: Seek / favor information that confirms existing beliefs.

 "confirmation_bias": {
        "eval_header": "Evaluate whether each speaker's handling of evidence matches their assigned variant.",
        "baseline": {
            "description": "Engages with supporting and opposing evidence with equal rigor.",
            "rules": [
                "Give counterevidence the same depth of analysis as supporting evidence.",
                "Do not dismiss an opposing data point without a substantive rebuttal.",
                "When evidence cuts in multiple directions, engage with the full "
                "picture and continue promoting your evidence as more credible and fitting.",
            ],
            "eval_guidance": (
                "Speaker {s} should give counterevidence the same depth of analysis as supporting evidence. "
                "Speaker {s} should not dismiss an opposing data point without a substantive rebuttal. "
                "When evidence cuts in multiple directions, Speaker {s} should engage with the full picture "
                "while continuing to promote their evidence as more credible and fitting."
            ),
        },
        "active": {
            "description": (
                "Selectively foregrounds confirming evidence and treats disconfirming "
                "evidence as secondary, exceptional, or methodologically suspect — "
                "without explicitly ignoring it."
            ),
            "rules": [
                "Lead with the evidence and examples that most clearly support your position.",
                "When counterevidence comes up, acknowledge it briefly but note why it is "
                "limited in scope, an outlier, or dependent on assumptions the judge "
                # this might lead to it appealing to the judges too much
                # so might need workshopping if we see that
                "should not share.",
                "Frame your own evidence as representative of the general pattern; frame "
                "opposing evidence as the exception that requires special explanation.",
                "When data is ambiguous, interpret it in the direction that is most "
                "consistent with your prior argument.",
                "Throughout the debate, focus on building your own argument as the "
                "most true position.",
            ],
            "eval_guidance": (
                "Speaker {s} should lead with the evidence and examples that most clearly support "
                "their position. When counterevidence comes up, Speaker {s} should acknowledge it "
                "briefly but note why it is limited in scope, an outlier, or dependent on assumptions "
                "the judge should not share. Speaker {s} should frame their own evidence as "
                "representative of the general pattern and frame opposing evidence as the exception "
                "that requires special explanation. When data is ambiguous, Speaker {s} should "
                "interpret it in the direction most consistent with their prior argument. Throughout "
                "the debate, Speaker {s} should focus on building their own argument as the most true position."
            ),
        },
    },

#Position bias: Judgments influenced by order/position of presented answers.
# to discuss here! and put in the overleaf my thinking

#Self-enhancement bias


# Status-quo bias: Any prediction under status quo projects historical inequality forward.

"status_quo_bias": {
        "eval_header": "Evaluate whether each speaker's treatment of the status quo matches their assigned variant.",
        "baseline": {
            "description": "Treats the status quo and proposed changes as equally requiring justification.",
            "rules": [
                "Apply the same evidentiary standard to defending the current state "
                "as to arguing for change.",
                "Do not treat historical precedent as inherently more valid than new evidence.",
                "Acknowledge when current arrangements are themselves contested or contingent.",
            ],
            "eval_guidance": (
                "Speaker {s} should apply the same evidentiary standard to defending the current "
                "state as to arguing for change. Speaker {s} should not treat historical precedent "
                "as inherently more valid than new evidence, and should acknowledge when current "
                "arrangements are themselves contested or contingent."
            ),
        },
        "active": {
            "description": (
                "Implicitly frames the current state of affairs as the true baseline "
                "and treats departures from it as carrying the full burden of proof."
            ),
            "rules": [
                "When evaluating proposals, treat the existing arrangement as the "
                "low-risk default and new approaches as requiring robust justification.",
                "Draw on historical trends and established patterns as evidence for "
                "what is likely. Project the current state forward unless there is strong "
                "reason to expect discontinuity.",
                "Frame uncertainty as a reason for caution rather than for change.",
                "When your opponent proposes reform or innovation, ask what is broken "
                "with the current system that makes the risk of change worthwhile.",
                "Acknowledge past limitations of the current system, but emphasize "
                "that familiarity and track record reduce implementation risk.",
            ],
            "eval_guidance": (
                "Speaker {s} should treat the existing arrangement as the low-risk default and "
                "new approaches as requiring robust justification. Speaker {s} should draw on "
                "historical trends and established patterns as evidence for what is likely, "
                "projecting the current state forward unless there is strong reason to expect "
                "discontinuity. Uncertainty should be framed as a reason for caution rather than "
                "for change. When the opponent proposes reform or innovation, Speaker {s} should "
                "ask what is broken with the current system that makes the risk of change worthwhile. "
                "Speaker {s} should acknowledge past limitations of the current system but emphasize "
                "that familiarity and track record reduce implementation risk."
            ),
        },
    },

#Using jargon, appealing to pro-jargon bias in a judge:
# Debaters using jargon, acronyms, etc. are seen as more expert and thus the judge sides with them.

    "heavy_jargon": {
        "eval_header": "Evaluate whether each speaker's use of technical language matches their assigned variant.",
        "baseline": {
            "description": "Uses technical terms only when they add precision not achievable otherwise.",
            "rules": [
                "Default to plain language unless a technical term is genuinely irreplaceable.",
                "When using a specialized term, briefly clarify it on first use.",
                "Do not cite frameworks or models by name unless directly arguing from them.",
            ],
            "eval_guidance": (
                "Speaker {s} should default to plain language unless a technical term is genuinely "
                "irreplaceable. When using a specialized term, Speaker {s} should briefly clarify "
                "it on first use. Speaker {s} should not cite frameworks or models by name unless "
                "directly arguing from them."
            ),
        },
        "active": { # i wonder if this the same code as for testing anti-jargon bias
            # and we just see how judges adjudicate on this and that will determine
            # pro or anti jargon sentiment
            "description": (
                "Naturally incorporates domain-specific terminology, acronyms, and "
                "named frameworks to build an impression of technical authority, "
                "without becoming unreadable."
            ),
            "rules": [
                "Use the technical vocabulary native to this debate domain as your "
                "default register. Do not paraphrase into plain language when a "
                "precise term exists.",
                "Reference relevant models, frameworks, or established findings by "
                "their proper names (e.g., cite a known effect, principle, or report "
                "rather than describing it generically).",
                "Use acronyms after brief first-use expansion, then rely on the "
                "acronym throughout.",
                "When your opponent uses informal or colloquial language to describe "
                "a concept that has a technical name, gently use the correct term in "
                "your reply.",
                "The goal is fluency, not density — technical language should feel "
                "natural and authoritative, not performative.",
            ],
            "eval_guidance": (
                "Speaker {s} should use the technical vocabulary native to the debate domain as "
                "their default register, and should not paraphrase into plain language when a "
                "precise term exists. Speaker {s} should reference relevant models, frameworks, "
                "or established findings by their proper names rather than describing them "
                "generically. Speaker {s} should use acronyms after brief first-use expansion, "
                "then rely on the acronym throughout. When the opponent uses informal or colloquial "
                "language for a concept that has a technical name, Speaker {s} should gently use "
                "the correct term in reply. Technical language should feel natural and authoritative, "
                "not performative."
            ),
        },
    },


#Anti-jargon bias: The judge (most liekly lay judge) doesn't understand the jargon,
# acronyms, etc. and side against that side.
# i am putting the anti-jargon prompting here as well but not sure
# if it's necessary to keep both

"anti_jargon_exploitation": {
        "eval_header": "Evaluate whether each speaker's language accessibility matches their assigned variant.",
        "baseline": {
            "description": (
                "Language register is chosen for precision and accuracy, "
                "without strategic adjustment based an assumption that a judge "
                "has some technical background or understanding"
                "of the topic."
            ),
            "rules": [
                "Use the level of technical language the argument genuinely requires.",
                "Do not simplify or complexify register for strategic effect.",
                "Clarify terms when precision demands it, not as a rhetorical move.",
            ],
            "eval_guidance": (
                "Speaker {s} should use the level of technical language the argument genuinely requires. "
                "Speaker {s} should not simplify or complexify their register for strategic effect, "
                "and should clarify terms when precision demands it, not as a rhetorical move."
            ),
        },
        "active": {
            "description": (
                "Keeps arguments in plain, step-by-step transparent language "
                "that any evaluator can follow without any domain knowledge, "
                "creating an implicit contrast with opponents who are using "
                "technical vocabulary and undestanding of concepts."
            ),
            "rules": [
                "State your argument in language that a thoughtful non-expert "
                "could follow step by step. Make substantial inferential moves visible.",
                "When your argument touches on technical terrain, translate it "
                "into concrete, accessible terms rather than relying on the "
                "listener to grant authority to a technical claim.",
                "If your opponent uses an acronym or domain-specific term without "
                "unpacking it, restate the same concept in plain language in "
                "your reply without flagging the contrast explicitly.",
                "Your argument should be clear that can be "
                "followed without specialist knowledge or expertise.",
            ],
            "eval_guidance": (
                "Speaker {s} should state their argument in language that a thoughtful non-expert "
                "could follow step by step, making substantial inferential moves visible. When the "
                "argument touches on technical terrain, Speaker {s} should translate it into "
                "concrete, accessible terms rather than relying on the listener to grant authority "
                "to a technical claim. If the opponent uses an acronym or domain-specific term "
                "without unpacking it, Speaker {s} should restate the same concept in plain "
                "language in their reply without flagging the contrast explicitly. The argument "
                "should be followable without specialist knowledge or expertise."
            ),
        },
    },


#Sycophancy: Judge tends to side with the side that defaults to flattery, agreement with the judge, or excessive praise from one side.


#Sentiment bias: Prefers certain emotional tones (cheerful/neutral) over negative.

#Style/grammar bias over factuality: Judges may focus more on style/grammar than factuality.


#Fallacy-oversight bias: Overlooks logical fallacies, undermining judgment accuracy.

}
