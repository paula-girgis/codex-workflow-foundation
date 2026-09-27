# Codex Workflow Foundation v0.1.4

أساس خفيف للمشاريع الجديدة وللتغييرات في المشاريع الموجودة. اختار حجم الشغل والأدوات حسب المشروع؛ مفيش framework أو database أو hosting مفروض. ده مش تطبيق جاهز ولا orchestrator.

للاستخدام مباشرة: اختار واحد من [الـ6 prompts الجاهزة](docs/STARTER-PROMPTS.md). المطلوب منك مسار المشروع، brief والقيود؛ المساعد يتولى التبنّي والخطة والـcheckpoints والأدلة. راجع [حدود اللي اتجرب](docs/READINESS.md) و[التغييرات](docs/CHANGELOG.md).

## ابدأ من هنا

افتح **مجلد المشروع الهدف** في Codex، مش مجلد الحزمة، عندما تبدأ شغلًا فعليًا. ابعت للمساعد مسار الحزمة `[FOUNDATION]` ومسار المشروع `[PROJECT]` داخل prompt؛ الحزمة لا تحتاج تكون parent للمشروع. لو المشروع جديد، أنشئ مجلدًا فارغًا أو مكانًا وافقت عليه؛ لو موجود، افتحه كما هو. الـagent يقرأ تعليمات المشروع أولًا ثم يشغّل `adopt` من مسار الحزمة، ويحافظ على `AGENTS.md` وملفات الـskills والقرارات الموجودة بدل الكتابة فوقها.

1. اقرأ تعليمات المشروع الحالية و[قواعد العمل](AGENTS.md).
2. سجّل الهدف والقيود والـstack والأدوات ومعايير القبول في `project/PROFILE.md`.
3. اختار المسار: bug صغير → reproduce / fix / verify؛ شغل بدون UI → standard؛ شاشات أو رحلة UI جديدة → visual.
4. اقرأ [المراحل والبوابات](docs/WORKFLOW.md) و[سياسة المعمارية](docs/ARCHITECTURE.md). فعّل [UI](docs/UI.md) فقط لما ينطبق.
5. استأنف من سجل التنفيذ، افحص الملفات، واشتغل في increment صغير قابل للتحقق. الأدلة والاعتمادات تخص نسخًا محددة.

## التثبيت المحلي في مشروع — بدون downloads

Python 3.10+ مطلوب للـhelper؛ النسخة اللي اتجربت مذكورة في سجل اختبار الحزمة. من جذر الحزمة دي نفّذ، بعد استبدال المسار بمشروعك:

```powershell
# مشروع جديد (المجلد فقط، مش scaffold لتطبيق)
python tools/workflow.py adopt --target 'D:\Projects\MyProject' --ui

# مشروع موجود: يحتفظ بالتعليمات والقرارات والملفات الحالية
python tools/workflow.py adopt --target 'D:\Projects\ExistingProject' --kind bug
```

بدون `--ui` تختار مسار standard؛ `--kind bug` يختار lightweight. استخدم `--ui` للتغييرات اللي محتاجة بوابات تصميم حتى لو مسماها bug. انسخ الاحتياجات الحقيقية للـprofile؛ القوالب مفيهاش موافقات ولا نتائج اختبارات موروثة.

التبنّي بيحط الأساس تحت `.workflow/`، والـskills تحت `.agents/skills/`، والاختيارات والحالة تحت `project/`. لو `AGENTS.md` موجود، **مش بيتعدل**: اطلب من Codex صراحةً قراءة `.workflow/START.md`، وبعد مراجعتك ادمج الإشارة في تعليماتك لو مناسب. لو مش موجود، الـhelper بيكتب رابط تعليمات صغير. مفيش تغيير لتعليمات المجلد الأب.

من داخل المشروع المتبنّي:

```powershell
python .workflow/tools/workflow.py resume
python .workflow/tools/workflow.py validate
python .workflow/tools/workflow.py select --kind bug
# select بيعرض خطة؛ مبيعدّلش الحالة.
```

قول لـCodex: «اقرأ `.workflow/START.md` و`project/PROFILE.md` واستأنف من `project/state.json`، وافحص الواقع قبل المتابعة». ممكن تستخدم skill `resume-project` لو الجلسة اكتشفتها؛ وجود الملف لا يثبت إنها اتحمّلت في جلسة مفتوحة بالفعل.

## سجل التنفيذ والحفظ

`project/state.json` هو المصدر الوحيد لحالة مشروع متبنّي. في الاستخدام العادي، الـagent مسؤول عن تحديث الحالة والـhashes والأدلة والحفظ؛ المستخدم مش مطلوب منه يعدّل JSON. الأوامر التالية مرجع للمساعد أو للصيانة اليدوية عند الحاجة. الـagent يسجّل التغيير في candidate منفصل، ويرفع `revision` بواحد، ثم:

```powershell
python .workflow/tools/workflow.py checkpoint --candidate project/state.candidate.json --expected-revision 1
```

استبدل `1` برقم النسخة الحالية. سجّل hashes الملفات والأدلة طبقًا للـschema؛ متجدّدش hash الدليل القديم كأنه اختبار جديد. شوف [الاستئناف والحفظ](docs/RECOVERY.md) للتفاصيل وحدود الضمان.

## خريطة التعديل

| عايز تغيّر | المكان المسؤول |
|---|---|
| مبادئ ومراحل workflow العامة | `docs/WORKFLOW.md` في مصدر الحزمة، ثم تحديث مراجع |
| قواعد جودة الكود والمعمارية | `docs/ARCHITECTURE.md` |
| قرارات المشروع والـstack وأوامر الاختبار | `project/PROFILE.md` وقرارات المشروع |
| بوابات تنفيذية أو عقد state | `schema/state.schema.json` + `tools/state.py` + اختبارات ومراجعة migration |
| الأدوات والإعداد | `docs/TOOLCHAIN.md`؛ حالة الأداة الفعلية في profile |
| سلوك checkpoint والاستئناف | `tools/state.py` و`docs/RECOVERY.md` |
| التبنّي والتحديث والميلستون | `tools/distribution.py` و`docs/ADOPTION.md` |
| theme/logo/shared components | ملفات التطبيق اللي تحددها خريطة [UI](docs/UI.md)، مش ملفات workflow |

## إيه آلي وإيه محتاج حكم وموافقة؟

- **آلي:** شكل state، المراجع والدورات، أدلة الإكمال، سجلات الاعتماد المطلوبة، ملفات مفقودة وhashes متغيرة، حماية checkpoint وتعارضات update.
- **مراجعة:** جودة المعمارية والتصميم، كفاية السيناريوهات، صحة اختيار الملفات اللي الاختبار يغطيها.
- **تعليمات:** تشغيل الفحوص، حفظ التقدم، عدم تجاوز المراحل، احترام الملكية. Markdown مش قفل تقني على agent.
- **موافقة مستخدم فعلية:** wireframes ثم polished designs؛ قرارات المنتج الجوهرية، والنشر/التكلفة/الوصول الخارجي حسب التفويض. كتابة `source: user` مش إثبات هوية أو موافقة؛ لازم أصل قابل للمراجعة.

## الحزمة نفسها

`templates/` نظيفة لإعادة الاستخدام. `development/` في نسخة التطوير تخص تنفيذ الحزمة فقط، ومش بتنتقل مع adoption ولا ZIP التوزيع النظيف. ZIP فيه tests للصيانة، بدون نتائج أو state مكتمل. استئناف تطوير النسخة الأصلية اللي فيها development:

```powershell
python tools/workflow.py resume --state development/state.json
python tests/run_acceptance.py
```

ابدأ بـ[التبنّي والتحديث وGitHub](docs/ADOPTION.md)، و[خطة النشر على GitHub](docs/GITHUB-PUBLICATION.md)، و[الأدوات](docs/TOOLCHAIN.md)، و[أمثلة هياكل التطبيقات](examples/APPLICATIONS.md). مفيش Git remote أو نشر أو backup خارجي متجهز تلقائيًا.
