import unittest
from parser import load_instance

class TestJSPParser(unittest.TestCase):
    
    # مسار ملف الـ benchmarks (تأكد من مطابقته لمكان الملف لديك)
    FILE_PATH = "Data/jobshop1.txt"

    def test_ft06_specifics(self):
        """اختبار تفصيلي لـ ft06 (الأبعاد، العمليات الأولى والأخيرة)"""
        try:
            jsp = load_instance(self.FILE_PATH, "ft06")
        except FileNotFoundError:
            self.skipTest("ملف البيانات غير موجود في المسار المحدد.")

        # التحقق من الأبعاد الأساسية
        self.assertEqual(jsp.n_jobs, 6)
        self.assertEqual(jsp.n_machines, 6)
        self.assertEqual(jsp.total_operations, 36)

        # التحقق من أول عملية في أول job
        first_op = jsp.jobs[0].operations[0]
        # بناءً على هيكل ملف ft06 القياسي
        self.assertIsNotNone(first_op)

        # التحقق من آخر عملية في آخر job (العملية الأخيرة في المهمة الأخيرة)
        last_op = jsp.jobs[5].operations[5]
        self.assertEqual(last_op.machine, 2)
        self.assertEqual(last_op.duration, 1)

    def test_benchmarks_loop(self):
        """اللف على مجموعة من الـ benchmarks والتحقق من الأبعاد وشروط الـ Job Shop"""
        benchmarks = [
            ("ft06", 6, 6),
            ("ft10", 10, 10),
            ("la01", 10, 5),
            ("abz5", 10, 10),
            ("orb01", 10, 10)
        ]

        for name, exp_jobs, exp_mach in benchmarks:
            with self.subTest(name=name):
                try:
                    jsp = load_instance(self.FILE_PATH, name)
                except FileNotFoundError:
                    self.skipTest("ملف البيانات غير موجود في المسار المحدد.")

                # 1. التحقق من الأبعاد ومطابقة total_operations
                self.assertEqual(jsp.n_jobs, exp_jobs)
                self.assertEqual(jsp.n_machines, exp_mach)
                self.assertEqual(jsp.total_operations, exp_jobs * exp_mach)

                # 2. التحقق أن كل job يحتوي على جميع الـ machines من 0 إلى n_machines - 1 مرة واحدة بالضبط
                for job in jsp.jobs:
                    self.assertEqual(job.n_operations, exp_mach)
                    machines = [op.machine for op in job.operations]
                    self.assertEqual(sorted(machines), list(range(exp_mach)))

    def test_error_cases(self):
        """اختبار الحالات الخاطئة والأخطاء المتوقعة"""
        # 1. اسم instance غير موجود تماماً
        with self.assertRaises(ValueError):
            load_instance(self.FILE_PATH, "xyz")

        # 2. التأكد من عدم الخلط بين ft1 و ft10 (ft1 غير موجود كاسم مستقل)
        with self.assertRaises(ValueError):
            load_instance(self.FILE_PATH, "ft1")

        # 3. مسار ملف خاطئ أو غير موجود
        with self.assertRaises(FileNotFoundError):
            load_instance("wrong_path_to_benchmarks.txt", "ft06")


if __name__ == "__main__":
    unittest.main()